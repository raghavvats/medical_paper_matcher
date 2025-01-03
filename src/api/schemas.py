from typing import Dict, Any

# MongoDB collection schemas
PROFILE_COLLECTION_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "physical", "demographics", "medical_history", "lifestyle"],
            "properties": {
                "_id": {"bsonType": "string"},
                "physical": {
                    "bsonType": "object",
                    "required": ["age", "weight", "sex", "height"],
                    "properties": {
                        "age": {"bsonType": "int"},
                        "weight": {"bsonType": "double"},
                        "sex": {"enum": ["male", "female"]},
                        "height": {"bsonType": "double"}
                    }
                },
                "demographics": {
                    "bsonType": "object",
                    "required": ["race", "location"],
                    "properties": {
                        "race": {"enum": ["asian", "black", "hispanic", "white", "other"]},
                        "location": {"enum": ["north_america", "south_america", "europe", "asia", "africa", "oceania", "antarctica"]}
                    }
                }
                # ... add other nested schemas as needed
            }
        }
    }
}

PAPER_COLLECTION_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "title", "content", "processed_data"],
            "properties": {
                "_id": {"bsonType": "string"},
                "title": {"bsonType": "string"},
                "content": {"bsonType": "string"},
                "processed_data": {
                    "bsonType": "object",
                    "required": ["ideal_profile", "conditions", "summary"],
                    "properties": {
                        "ideal_profile": {"bsonType": "object"},
                        "conditions": {"bsonType": "string"},
                        "summary": {"bsonType": "string"}
                    }
                }
            }
        }
    }
} 