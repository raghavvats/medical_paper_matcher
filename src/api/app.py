from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .models import ProfileResponse, MatchResponse, PaperMatch, PaperUploadResponse, ErrorResponse, UserProfileResponse, SaveProfileRequest
from src.models.profile import CustomerProfile
from src.core.profile_matcher import ProfileMatcher
from src.core.paper_processor import PaperProcessor
from src.ai.openai_client import OpenAIClient
from .database import Database
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
import uuid
import tempfile
import os
import base64
from typing import List

app = FastAPI(
    title="Research Paper Matcher",
    description="Match patient profiles with relevant research papers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await Database.connect_db()
    # Initialize GridFS with the correct class
    app.fs = AsyncIOMotorGridFSBucket(Database.get_db())

@app.on_event("shutdown")
async def shutdown_db_client():
    await Database.close_db()

@app.post("/match/", response_model=MatchResponse)
async def match_papers(profile: CustomerProfile):
    """
    Match a profile against stored papers and return matching results.
    """
    try:
        db = Database.get_db()
        profile_matcher = ProfileMatcher()
        
        # Get all papers from database
        papers = await db.papers.find().to_list(length=None)
        matches = []
        
        print(f"Found {len(papers)} papers to check for matches")
        
        # Convert profile to dict and convert Enum values to strings
        profile_dict = profile.dict()
        
        # Convert Enum values in physical
        profile_dict['physical']['sex'] = profile_dict['physical']['sex'].value
        
        # Convert Enum values in demographics
        profile_dict['demographics']['race'] = profile_dict['demographics']['race'].value
        profile_dict['demographics']['location'] = profile_dict['demographics']['location'].value
        
        # Convert Enum values in medical_history lists
        profile_dict['medical_history']['preexisting_conditions'] = [
            condition.value for condition in profile_dict['medical_history']['preexisting_conditions']
        ]
        profile_dict['medical_history']['prior_conditions'] = [
            condition.value for condition in profile_dict['medical_history']['prior_conditions']
        ]
        profile_dict['medical_history']['surgeries'] = [
            surgery.value for surgery in profile_dict['medical_history']['surgeries']
        ]
        profile_dict['medical_history']['active_medications'] = [
            med.value for med in profile_dict['medical_history']['active_medications']
        ]
        
        # Convert Enum values in lifestyle
        profile_dict['lifestyle']['athleticism'] = profile_dict['lifestyle']['athleticism'].value
        profile_dict['lifestyle']['diet'] = profile_dict['lifestyle']['diet'].value
        
        print(f"Processing profile with characteristics: {profile_dict}")
        
        for paper in papers:
            try:
                print(f"Checking paper: {paper['_id']} - {paper['title']}")
                
                paper_data = {
                    'ideal_profile': paper['processed_data']['ideal_profile'],
                    'conditions': paper['processed_data']['conditions']
                }
                
                is_match = profile_matcher._is_match(profile_dict, paper_data)
                print(f"Match result for paper {paper['_id']}: {is_match}")
                
                if is_match:
                    match = PaperMatch(
                        paper_id=paper['_id'],
                        title=paper['title'],
                        summary=paper['processed_data']['summary'],
                        match_score=1.0,
                        download_url=f"/papers/{paper['_id']}/download"
                    )
                    matches.append(match)
                    print(f"Added match: {match}")
            except Exception as e:
                print(f"Error processing paper {paper.get('_id', 'unknown')}: {str(e)}")
                continue
        
        print(f"Total matches found: {len(matches)}")
        response = MatchResponse(
            profile_id="temporary",
            matches=matches,
            total_matches=len(matches)
        )
        print(f"Returning response with {len(response.matches)} matches")
        return response
        
    except Exception as e:
        print(f"Match error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process match request: {str(e)}"
        )

@app.post("/papers/upload/", response_model=List[PaperUploadResponse])
async def upload_papers(files: List[UploadFile] = File(...)):
    """
    Upload and process multiple papers. Stores the papers and their processed data in MongoDB.
    """
    responses = []
    
    for file in files:
        tmp_path = None
        try:
            # Validate file type
            if not file.filename.endswith('.pdf'):
                responses.append(PaperUploadResponse(
                    paper_id="",
                    title=file.filename,
                    message=f"Skipped: File must be a PDF"
                ))
                continue

            # Read the file content
            content = await file.read()
            print(f"Processing file {file.filename}, size: {len(content)} bytes")

            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            # Process the PDF
            processor = PaperProcessor(papers_dir=os.path.dirname(tmp_path))
            text = processor.extract_text_from_pdf(os.path.basename(tmp_path))
            
            if not text:
                responses.append(PaperUploadResponse(
                    paper_id="",
                    title=file.filename,
                    message="Failed to extract text from PDF"
                ))
                continue
            
            # Analyze with OpenAI
            ai_client = OpenAIClient()
            try:
                analysis = await ai_client.analyze_paper(text)
            except Exception as e:
                responses.append(PaperUploadResponse(
                    paper_id="",
                    title=file.filename,
                    message=f"OpenAI analysis failed: {str(e)}"
                ))
                continue
            
            # Generate paper_id and store in GridFS
            paper_id = str(uuid.uuid4())
            await app.fs.upload_from_stream(
                paper_id,
                content,
                metadata={"content_type": "application/pdf"}
            )
            
            # Store metadata in database
            paper_data = {
                "_id": paper_id,
                "title": file.filename,
                "content": text,
                "processed_data": {
                    "ideal_profile": analysis["ideal_profile"],
                    "conditions": analysis["conditions"],
                    "summary": analysis["summary"]
                }
            }
            
            db = Database.get_db()
            await db.papers.insert_one(paper_data)
            
            responses.append(PaperUploadResponse(
                paper_id=paper_id,
                title=file.filename,
                summary=analysis["summary"],
                message="Paper successfully processed"
            ))
            
        except Exception as e:
            responses.append(PaperUploadResponse(
                paper_id="",
                title=file.filename,
                message=f"Error processing paper: {str(e)}"
            ))
            
        finally:
            # Clean up temporary file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    print(f"Error deleting temporary file: {e}")
    
    return responses

@app.get("/")
async def root():
    return {"message": "Welcome to the Research Paper Matcher API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/papers/{paper_id}/view")
async def get_paper_pdf(paper_id: str):
    try:
        print(f"Attempting to retrieve PDF with ID: {paper_id}")
        # Get PDF from GridFS using the correct method
        try:
            grid_out = await app.fs.open_download_stream_by_name(paper_id)
        except Exception as e:
            print(f"Error opening GridFS stream: {str(e)}")
            raise HTTPException(status_code=404, detail=f"PDF not found in GridFS: {str(e)}")

        try:
            pdf_content = await grid_out.read()
            print(f"Retrieved PDF content length: {len(pdf_content) if pdf_content else 0} bytes")
            
            if not pdf_content:
                raise HTTPException(status_code=404, detail="PDF content is empty")
            
            # Convert to base64 for frontend
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            print(f"Base64 content length: {len(pdf_base64)} characters")
            
            return {
                "pdf_content": pdf_base64,
                "content_type": "application/pdf"
            }
        except Exception as e:
            print(f"Error reading PDF content: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to read PDF content: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error retrieving PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") 

@app.post("/profiles/save", response_model=UserProfileResponse)
async def save_user_profile(request: SaveProfileRequest):
    """
    Save or update a user profile.
    """
    try:
        success = await Database.save_user_profile(request.username, request.profile)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to save profile")
            
        saved_profile = await Database.get_user_profile(request.username)
        return UserProfileResponse(
            username=saved_profile["username"],
            profile=saved_profile["profile"],
            last_updated=saved_profile["last_updated"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profiles/{username}", response_model=UserProfileResponse)
async def get_user_profile(username: str):
    """
    Retrieve a user's saved profile.
    """
    try:
        profile = await Database.get_user_profile(username)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        return UserProfileResponse(
            username=profile["username"],
            profile=profile["profile"],
            last_updated=profile["last_updated"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.delete("/profiles/{username}")
async def delete_user_profile(username: str):
    """
    Delete a user profile.
    """
    try:
        success = await Database.delete_user_profile(username)
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {"message": f"Profile {username} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/papers/{paper_id}")
async def delete_paper(paper_id: str):
    """
    Delete a paper and its associated PDF from the database.
    """
    try:
        # Delete PDF from GridFS
        try:
            await app.fs.delete(paper_id)
        except Exception as e:
            print(f"Error deleting PDF from GridFS: {e}")
            # Continue even if GridFS deletion fails
            
        # Delete paper metadata from papers collection
        db = Database.get_db()
        result = await db.papers.delete_one({"_id": paper_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Paper not found")
            
        return {"message": f"Paper {paper_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/papers")
async def get_papers():
    """
    Get all papers in the database.
    """
    try:
        db = Database.get_db()
        papers = await db.papers.find().to_list(length=None)
        return papers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 