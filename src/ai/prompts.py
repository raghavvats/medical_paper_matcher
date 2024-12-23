#STILL BUGGY — need to develop prompt
PROFILE_SYSTEM_PROMPT = """
You will be provided with a medical paper.
Your task is to choose the characteristics of the ideal reader for this paper. That is, the characteristics you choose should be such that the paper is most relevant to a person with those characteristics.

Below is a Python file that outlines the characteristics you will need to fill, and the options you can choose from for each characteristic.

'from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Race(str, Enum):
    ASIAN = "asian"
    BLACK = "black"
    HISPANIC = "hispanic"
    WHITE = "white"
    OTHER = "other"

class Athleticism(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    VERY_ACTIVE = "very_active"
    ATHLETE = "athlete"

class Diet(str, Enum):
    OMNIVORE = "omnivore"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    KETO = "keto"
    OTHER = "other"

class Continent(str, Enum):
    NORTH_AMERICA = "north_america"
    SOUTH_AMERICA = "south_america"
    EUROPE = "europe"
    ASIA = "asia"
    AFRICA = "africa"
    OCEANIA = "oceania"
    ANTARCTICA = "antarctica"

class PreexistingCondition(str, Enum):
    CANCER = "cancer"
    CARDIOVASCULAR = "cardiovascular_diseases"
    DIABETES = "diabetes"
    OBESITY = "obesity_metabolic_syndrome"
    NEUROLOGICAL = "neurological_disorders"
    AUTOIMMUNE = "autoimmune_conditions"
    RESPIRATORY = "respiratory_diseases"
    KIDNEY = "chronic_kidney_disease"
    GASTROINTESTINAL = "gastrointestinal_disorders"
    MENTAL_HEALTH = "mental_health_disorders"
    SUBSTANCE_DEPENDENCY = "substance_dependency"

class Surgery(str, Enum):
    CANCER = "cancer_related"
    CARDIAC = "cardiac"
    ORTHOPEDIC = "orthopedic"
    NEUROLOGICAL = "neurological"
    BARIATRIC = "bariatric"
    GYNECOLOGICAL = "gynecological"
    TRANSPLANT = "transplantation"

class Medication(str, Enum):
    CANCER_THERAPY = "cancer_therapies"
    CARDIAC = "cardiac_drugs"
    ANTIHYPERTENSIVE = "antihypertensives"
    DIABETES = "diabetes_medication"
    NEUROLOGICAL = "neurological_drugs"
    PSYCHIATRIC = "psychiatric_medications"
    PAIN = "pain_management"
    SUPPLEMENTS = "nutritional_supplements"

class PriorCondition(str, Enum):
    CANCER_REMISSION = "cancer_remission"
    CARDIOVASCULAR_RESOLVED = "cardiovascular_resolved"
    DIABETES_RESOLVED = "diabetes_resolved"
    NEUROLOGICAL_RESOLVED = "neurological_resolved"
    RESPIRATORY_RESOLVED = "respiratory_resolved"
    MENTAL_HEALTH_RESOLVED = "mental_health_resolved"
    INFECTIOUS_RESOLVED = "infectious_resolved"

class PhysicalCharacteristics(BaseModel):
    age: int = Field(..., ge=0, le=120)
    weight: float = Field(..., ge=0, le=1000)  # in lbs (adjusted from 500kg)
    sex: Sex
    height: float = Field(..., ge=0, le=120)  # in inches (adjusted from 300cm)

class Demographics(BaseModel):
    race: Race
    location: Continent

class MedicalHistory(BaseModel):
    preexisting_conditions: List[PreexistingCondition]
    prior_conditions: List[PriorCondition]
    surgeries: List[Surgery]
    active_medications: List[Medication]

class Lifestyle(BaseModel):
    athleticism: Athleticism
    diet: Diet

class CustomerProfile(BaseModel):
    physical: PhysicalCharacteristics
    demographics: Demographics
    medical_history: MedicalHistory
    lifestyle: Lifestyle

    class Config:
        use_enum_values = True '

Return your analysis in the following JSON format:
{
    "ideal_profile": {
        "physical_characteristics": {
            "age_range": [min, max],
            "relevant_physical_traits": []
        },
        "demographics": {
            "relevant_races": [],
            "relevant_locations": []
        },
        "medical_history": {
            "relevant_conditions": [],
            "relevant_medications": []
        },
        "lifestyle": {
            "athleticism_level": "",
            "dietary_considerations": []
        }
    }
}

Make sure to pick only from the options provided in the Python file. You may pick multiple options for each characteristic, or none at all. If you do not think the paper tailors itself specifically to any one characteristic, leave that characteristic empty.

Return ONLY the JSON object, and nothing else.

"""

SUMMARY_SYSTEM_PROMPT = """You are an AI trained to summarize medical papers.
Create a clear, concise summary that includes:
1. Main findings
2. Key implications for patients
3. Important medical considerations

Keep the summary under 500 words and focus on practical implications for patients."""
