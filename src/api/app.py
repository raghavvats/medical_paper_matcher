from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .models import ProfileResponse, MatchResponse, PaperMatch, PaperUploadResponse, ErrorResponse
from src.models.profile import CustomerProfile
from src.core.profile_matcher import ProfileMatcher
from src.core.paper_processor import PaperProcessor
from src.ai.openai_client import OpenAIClient
from .database import Database
import uuid
import tempfile
import os

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
        
        print(f"Converted profile: {profile_dict}")
        
        for paper in papers:
            print(f"Checking paper: {paper['_id']}")
            
            paper_data = {
                'ideal_profile': paper['processed_data']['ideal_profile'],
                'conditions': paper['processed_data']['conditions']
            }
            
            if profile_matcher._is_match(profile_dict, paper_data):
                matches.append(PaperMatch(
                    paper_id=paper['_id'],
                    title=paper['title'],
                    summary=paper['processed_data']['summary'],
                    match_score=1.0,
                    download_url=f"/papers/{paper['_id']}/download"
                ))
        
        print(f"Found {len(matches)} matches")
        return MatchResponse(
            profile_id="temporary",
            matches=matches,
            total_matches=len(matches)
        )
        
    except Exception as e:
        print(f"Match error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process match request: {str(e)}"
        )

@app.post("/papers/upload/", response_model=PaperUploadResponse)
async def upload_paper(file: UploadFile = File(...)):
    """
    Upload and process a new paper. Stores the paper and its processed data in MongoDB.
    """
    tmp_path = None
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        # Create temporary file to store the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Process the PDF
        try:
            processor = PaperProcessor(papers_dir=os.path.dirname(tmp_path))
            text = processor.extract_text_from_pdf(os.path.basename(tmp_path))
            
            if not text:
                raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
            
            print(f"Successfully extracted text from PDF: {len(text)} characters")
            
            # Analyze with OpenAI
            ai_client = OpenAIClient()
            try:
                analysis = await ai_client.analyze_paper(text)
                print("Successfully analyzed paper with OpenAI")
            except Exception as e:
                print(f"OpenAI analysis failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"OpenAI analysis failed: {str(e)}")
            
            # Store in database
            paper_id = str(uuid.uuid4())
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
            try:
                await db.papers.insert_one(paper_data)
                print(f"Successfully stored paper in database with ID: {paper_id}")
            except Exception as e:
                print(f"Database storage failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Database storage failed: {str(e)}")
            
            return PaperUploadResponse(
                paper_id=paper_id,
                title=file.filename,
                summary=analysis["summary"]
            )
            
        except Exception as e:
            print(f"Error processing paper: {str(e)}")
            raise
            
    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as e:
                print(f"Error deleting temporary file: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Research Paper Matcher API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 