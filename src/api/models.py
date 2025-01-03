from typing import List, Optional
from pydantic import BaseModel

class PaperMatch(BaseModel):
    paper_id: str
    title: str
    summary: str
    match_score: float
    download_url: Optional[str] = None

class ProfileResponse(BaseModel):
    profile_id: str
    message: str = "Profile successfully created"

class MatchResponse(BaseModel):
    profile_id: str
    matches: List[PaperMatch]
    total_matches: int

class PaperUploadResponse(BaseModel):
    paper_id: str
    title: str
    message: str = "Paper successfully processed"
    summary: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str 