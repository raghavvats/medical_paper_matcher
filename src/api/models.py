from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from datetime import datetime
from src.models.profile import CustomerProfile

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

class SaveProfileRequest(BaseModel):
    username: str
    profile: Union[Dict[str, Any], CustomerProfile]

    class Config:
        arbitrary_types_allowed = True

class UserProfileResponse(BaseModel):
    username: str
    profile: Dict[str, Any]
    last_updated: datetime 