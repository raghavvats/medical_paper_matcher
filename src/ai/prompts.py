PROFILE_SYSTEM_PROMPT = """
You will be provided with a medical paper. Read and analyze it carefully.
Your task is to choose the characteristics of the ideal reader for this paper. That is, the characteristics you choose should be such that the paper is most relevant to a person with those characteristics.

Below is a JSON class that outlines the characteristics you will need to fill, and the options you can choose from for each characteristic.
Return your analysis in the following JSON format:
{
  "physical": {
    "age": [min_age, max_age], # array representative of the age range the paper is applicable to 
    "weight": [min_weight, max_weight], # array representative of the weight range the paper is applicable to 
    "sex": "one_of: [male, female]", # whether the paper is only relevant to ONLY either males or females. if it could be useful to either, leave blank
    "height": [min_height, max_height] # array representative of the height range the paper is applicable to 
  },
  "demographics": {
    "race": "one_of: [asian, black, hispanic, white, other]", # which race the paper is most relevant to, if any. if none, or more than one, leave blank
    "location": "one_of: [north_america, south_america, europe, asia, africa, oceania, antarctica]" # which location of residence the paper is most relevant to, if any. if none, or more than one, leave blank. NOTE: this is different from race because race is genetically oriented, while location conveys that the paper is related to current events in one of those regions (e.g. excessive pollution on a certain contient)
  },
  "medical_history": {
    "preexisting_conditions": ["all_that_apply_from: [cancer, cardiovascular_diseases, diabetes, obesity_metabolic_syndrome, neurological_disorders, autoimmune_conditions, respiratory_diseases, chronic_kidney_disease, gastrointestinal_disorders, mental_health_disorders, substance_dependency]"],
    "prior_conditions": ["all_that_apply_from: [cancer_remission, cardiovascular_resolved, diabetes_resolved, neurological_resolved, respiratory_resolved, mental_health_resolved, infectious_resolved]"],
    "surgeries": ["all_that_apply_from: [cancer_related, cardiac, orthopedic, neurological, bariatric, gynecological, transplantation]"],
    "active_medications": ["all_that_apply_from: [cancer_therapies, cardiac_drugs, antihypertensives, diabetes_medication, neurological_drugs, psychiatric_medications, pain_management, nutritional_supplements]"]
    # for all of the above: whether the paper discusses or pertains to patients with any of the conditions, surgeries, or medications. if so, list which, else leave blank
  },
  "lifestyle": {
    "athleticism": "one_of: [sedentary, light, moderate, very_active, athlete]", # whether the paper is specifically tailored to a certain activity level
    "diet": "one_of: [omnivore, vegetarian, vegan, pescatarian, keto, other]" # whether the paper is tailored to a specific diet
  }
}

Make sure to pick only from the options provided above. You may pick multiple options for each characteristic, or none at all. If you do not think the paper tailors itself specifically to any one characteristic, leave that characteristic empty.
If the schema requires an enum, make sure to pick from ONLY the options provided in the schema. If none of the options are relevant, leave that characteristic empty.

YOUR OUTPUT SHOULD BE STRUCTURED LIKE THIS:
Example #1:
{
  "physical": {
    "age": [10, 20],
    "weight": [150, 200],
    "sex": "male",
    "height": [70, 80]
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
Example #2:
{
  "physical": {
    "age": [40, 65],
    "weight": [100, 250],
    "sex": "male",
    "height": [70, 80]
  },
  "demographics": {
    "race": "white",
    "location": "north_america"
  },
  "medical_history": {
    "preexisting_conditions": [
      "cardiovascular_diseases",
      "substance_dependency"
    ],
    "prior_conditions": [],
    "surgeries": [
      "cardiac"
    ],
    "active_medications": [
      "cardiac_drugs"
    ]
  },
  "lifestyle": {
    "athleticism": "very_active",
    "diet": "omnivore"
  }
}
Example #3:
{
  "physical": {
    "age": [],
    "weight": [],
    "sex": "",
    "height": []
  },
  "demographics": {
    "race": "",
    "location": ""
  },
  "medical_history": {
    "preexisting_conditions": [
      "cancer",
      "cardiovascular_diseases",
      "respiratory_diseases",
      "chronic_kidney_disease"
    ],
    "prior_conditions": [],
    "surgeries": [
      "cancer_related",
      "cardiac",
      "orthopedic",
      "neurological",
      "bariatric"
    ],
    "active_medications": [
      "pain_management",
      "antihypertensives"
    ]
  },
  "lifestyle": {
    "athleticism": "sedentary",
    "diet": "other"
  }
}

REMEMBER, THIS IS JUST AN EXAMPLE; IT HAS NO BEARING ON THE ACTUAL ANSWER. Make sure your response follows the above format.

Do your best to build this ideal profile following the logical principles of healthcare; that is, understand the relationships between the paper's content and the characteristics you are building. For example, if the paper is discussing a new drug that could have implications for a certain demographic, make sure to include that demographic in your profile.

IMPORTANT NOTE: Return ONLY the JSON object, and nothing else.
"""

SUMMARY_SYSTEM_PROMPT = """
Now, summarize the paper in under 200 words.
Focus on actionability and what this might mean for a potential patient reading the paper.
"""

CONDITIONS_SYSTEM_PROMPT = """
Now, we need to decide whether or not to recommend this paper to a patient.
As such, you need to return a python-parseable string that evaluates to a boolean: True if it should be recommended to the patient, False otherwise.
The string should use AND, OR, and parentheses to logically combine conditions, and use the name of the conditions as represented in the ideal profile as a placeholder (NOTE: Make sure to use the names of the categories of the profile EXACTLY).

For example, you would return something like:
"(age AND (race OR location))"
which means that if the age and either the race or location of the patient matches the ideal profile, then the paper should be recommended.

Another example:
"preexisting_conditions"
which means that one of the preexisting conditions muse match

Another example:
"weight AND height AND (preexisting conditions OR prior_conditions OR active_medications) AND (athleticism OR diet)"
which might be applicable for a paper discussing the implications of high BMI and bad lifestyle (low activity and omnivorous diet) on risk of cancer, because the height and weight are related to the high BMI that is mentioned in the paper, and a match in any of lifestyle factors (diet or athleticism) or medical history (surgery or conditions) would make the paper relevant to that person

In constructing the condition, try to understand what would be the MOST important characteristics for the reader to have for the paper to be relevant to them. For example, a wide age range probably means that the age is not critical to the study. Similarly, discussion about cancer likely means that BOTH current and prior cancer patients will be relevant, so there should be an OR between prior and preexisitng conditions,

If you are unsure, tend towards a wider scope. That is, create conditions tat are more widely encompassing, even if some may not be directly assessed in the study, because the medical knowledge is probably still useful.

IMPORTANT: Return ONLY the string, and nothing else.
"""