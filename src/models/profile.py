from enum import Enum
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
        use_enum_values = True 