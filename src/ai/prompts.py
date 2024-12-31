PROFILE_SYSTEM_PROMPT = """
You will be provided with a medical paper. Read and analyze it carefully.
Your task is to choose the characteristics of the ideal reader for this paper. That is, the characteristics you choose should be such that the paper is most relevant to a person with those characteristics.

Below is a JSON class that outlines the characteristics you will need to fill, and the options you can choose from for each characteristic.
Return your analysis in the following JSON format:
{
  "physical": {
    "age": [min_age, max_age],
    "weight": [min_weight, max_weight],
    "sex": "one_of: [male, female]",
    "height": [min_height, max_height]
  },
  "demographics": {
    "race": "one_of: [asian, black, hispanic, white, other]",
    "location": "one_of: [north_america, south_america, europe, asia, africa, oceania, antarctica]"
  },
  "medical_history": {
    "preexisting_conditions": ["all_that_apply_from: [cancer, cardiovascular_diseases, diabetes, obesity_metabolic_syndrome, neurological_disorders, autoimmune_conditions, respiratory_diseases, chronic_kidney_disease, gastrointestinal_disorders, mental_health_disorders, substance_dependency]"],
    "prior_conditions": ["all_that_apply_from: [cancer_remission, cardiovascular_resolved, diabetes_resolved, neurological_resolved, respiratory_resolved, mental_health_resolved, infectious_resolved]"],
    "surgeries": ["all_that_apply_from: [cancer_related, cardiac, orthopedic, neurological, bariatric, gynecological, transplantation]"],
    "active_medications": ["all_that_apply_from: [cancer_therapies, cardiac_drugs, antihypertensives, diabetes_medication, neurological_drugs, psychiatric_medications, pain_management, nutritional_supplements]"]
  },
  "lifestyle": {
    "athleticism": "one_of: [sedentary, light, moderate, very_active, athlete]",
    "diet": "one_of: [omnivore, vegetarian, vegan, pescatarian, keto, other]"
  }
}

Make sure to pick only from the options provided above. You may pick multiple options for each characteristic, or none at all. If you do not think the paper tailors itself specifically to any one characteristic, leave that characteristic empty.
If the schema requires an enum, make sure to pick from ONLY the options provided in the schema. If none of the options are relevant, leave that characteristic empty.

FOR EXAMPLE:
{
  "physical": {
    "age": [10, 20],
    "weight": [150.0, 200.0],
    "sex": "male",
    "height": [70.0, 80.0]
  },
  "demographics": {
    "race": "asian",
    "location": "north_america"
  },
  "medical_history": {
    "preexisting_conditions": [
      "cancer",
      "neurological_disorders",
      "respiratory_diseases"
    ],
    "prior_conditions": [
      "cardiovascular_resolved",
      "infectious_resolved",
      "respiratory_resolved"
    ],
    "surgeries": [],
    "active_medications": [
      "cardiac_drugs",
      "antihypertensives",
      "psychiatric_medications"
    ]
  },
  "lifestyle": {
    "athleticism": "athlete",
    "diet": "vegetarian"
  }
}
REMEMBER, THIS IS JUST AN EXAMPLE; IT HAS NO BEARING ON THE ACTUAL ANSWER. Make sure your response follows the above format.

Do your best to build this ideal profile following the logical principles of healthcare; that is, understand the relationships between the paper's content and the characteristics you are building. For example, if the paper is discussing a new drug that could have implications for a certain demographic, make sure to include that demographic in your profile.

IMPORTANT NOTE: Return ONLY the JSON object, and nothing else.
"""

SUMMARY_SYSTEM_PROMPT = """
Now, summarize the paper.
Keep the summary under 500 words and focus on practical implications for patients.
"""

CONDITIONS_SYSTEM_PROMPT = """
Now, we need to decide whether or not to recommend this paper to a patient.
As such, you need to return a python-parseable string that evaluates to a boolean: True if it should be recommended to the patient, False otherwise.
The string should use AND, OR, and parentheses to logically combine conditions, and use the name of the conditions as represented in the ideal profile as a placeholder.

For example, you would return something like:
"(age AND (race OR location))"
which means that if the age and either the race or location of the patient matches the ideal profile, then the paper should be recommended.

When constructing the string, try to reason through what the paper is about and to who it would be relevant. For example, if the study the paper discusses is only conducted on diabetic patients, then it is reasonable that that condition MUST apply for that paper to be relevant. On the other hand, if the study's participants are ages 6-70, then age is not relvant, because that range is so wide.

IMPORTANT: Return ONLY the string, and nothing else.
"""
