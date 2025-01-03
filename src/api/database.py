from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB."""
        cls.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client is not None:
            cls.client.close()
            
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if cls.client is None:
            raise ConnectionError("Database not initialized")
        return cls.client.research_papers 