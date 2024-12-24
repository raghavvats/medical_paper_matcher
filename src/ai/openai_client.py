from typing import Dict, List, Optional
import openai
from pathlib import Path
import json
import os
from .prompts import PROFILE_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key from environment or parameter."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass as parameter.")
        
        openai.api_key = self.api_key

    def analyze_paper(self, paper_text: str) -> Dict:
        """
        Analyze paper text to extract ideal reader profile and generate summary.
        
        Args:
            paper_text: The text content of the paper
        Returns:
            Dict containing:
                - ideal_profile: Dict of ideal reader characteristics
                - conditions: List of condition tokens for matching
                - summary: String containing paper summary
        """
        try:
            # First call: Get ideal profile and conditions
            profile_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": PROFILE_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Paper text:\n\n{paper_text}"}
                ]
            )
            
            profile_data = json.loads(profile_response.choices[0].message.content)
            
            # Second call: Get summary
            summary_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Using 3.5 for summary as it's cheaper
                messages=[
                    {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Paper text:\n\n{paper_text}"}
                ]
            )
            
            summary = summary_response.choices[0].message.content
            
            return {
                "ideal_profile": profile_data["ideal_profile"],
                "conditions": profile_data["conditions"],
                "summary": summary
            }
            
        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")
            raise

    def save_analysis(self, paper_name: str, analysis: Dict) -> None:
        """Save the analysis results to a JSON file."""
        output_dir = Path("data/papers/analyzed")
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / f"{paper_name}_analysis.json"
        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2)
