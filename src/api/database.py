from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
from datetime import datetime

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB."""
        try:
            cls.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
            cls.db = cls.client.research_matcher
            
            # Create indexes for user profiles
            await cls.db.user_profiles.create_index("username", unique=True)
            
            print("Connected to MongoDB.")
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise e

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        return cls.db

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed.")

    @classmethod
    async def save_user_profile(cls, username: str, profile_data: dict) -> bool:
        """
        Save or update a user profile.
        Returns True if successful, False if username already exists.
        """
        try:
            # Convert profile data to plain dict with string values
            processed_profile = {
                'physical': {
                    'age': profile_data['physical']['age'],
                    'weight': profile_data['physical']['weight'],
                    'height': profile_data['physical']['height'],
                    'sex': profile_data['physical']['sex'].value if hasattr(profile_data['physical']['sex'], 'value') else profile_data['physical']['sex']
                },
                'demographics': {
                    'race': profile_data['demographics']['race'].value if hasattr(profile_data['demographics']['race'], 'value') else profile_data['demographics']['race'],
                    'location': profile_data['demographics']['location'].value if hasattr(profile_data['demographics']['location'], 'value') else profile_data['demographics']['location']
                },
                'medical_history': {
                    'preexisting_conditions': [
                        cond.value if hasattr(cond, 'value') else cond 
                        for cond in profile_data['medical_history']['preexisting_conditions']
                    ],
                    'prior_conditions': [
                        cond.value if hasattr(cond, 'value') else cond 
                        for cond in profile_data['medical_history']['prior_conditions']
                    ],
                    'surgeries': [
                        surgery.value if hasattr(surgery, 'value') else surgery 
                        for surgery in profile_data['medical_history']['surgeries']
                    ],
                    'active_medications': [
                        med.value if hasattr(med, 'value') else med 
                        for med in profile_data['medical_history']['active_medications']
                    ]
                },
                'lifestyle': {
                    'athleticism': profile_data['lifestyle']['athleticism'].value if hasattr(profile_data['lifestyle']['athleticism'], 'value') else profile_data['lifestyle']['athleticism'],
                    'diet': profile_data['lifestyle']['diet'].value if hasattr(profile_data['lifestyle']['diet'], 'value') else profile_data['lifestyle']['diet']
                }
            }

            # Use upsert to either insert new or update existing
            result = await cls.db.user_profiles.update_one(
                {"username": username},
                {"$set": {
                    "username": username,
                    "profile": processed_profile,
                    "last_updated": datetime.utcnow()
                }},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving user profile: {e}")
            return False

    @classmethod
    async def get_user_profile(cls, username: str) -> Optional[dict]:
        """
        Retrieve a user profile by username.
        Returns None if not found.
        """
        try:
            profile = await cls.db.user_profiles.find_one({"username": username})
            return profile
        except Exception as e:
            print(f"Error retrieving user profile: {e}")
            return None

    @classmethod
    async def delete_user_profile(cls, username: str) -> bool:
        """
        Delete a user profile.
        Returns True if successful, False if not found or error.
        """
        try:
            result = await cls.db.user_profiles.delete_one({"username": username})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user profile: {e}")
            return False 