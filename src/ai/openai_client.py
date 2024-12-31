from dotenv import load_dotenv
load_dotenv()

from typing import Dict, List, Optional
from openai import OpenAI
from pathlib import Path
import json
import os
from .prompts import PROFILE_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT, CONDITIONS_SYSTEM_PROMPT

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = ""):
        """Initialize OpenAI client with API key from environment or parameter."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass as parameter.")
        
        self.client = OpenAI(api_key=self.api_key)

    def analyze_paper(self, paper_text: str) -> Dict:
        """
        Analyze paper text to extract ideal reader profile, conditions, and generate summary.
        Uses a single chat session with follow-up messages for each analysis component.
        
        Args:
            paper_text: The text content of the paper
        Returns:
            Dict containing:
                - ideal_profile: Dict of ideal reader characteristics
                - conditions: List of condition tokens for matching
                - summary: String containing paper summary
        """
        try:
            # Initialize chat for profile analysis
            messages = [
                {"role": "system", "content": PROFILE_SYSTEM_PROMPT},
                {"role": "user", "content": f"Paper text:\n\n{paper_text}"}
            ]
            
            # First call: Get ideal profile
            profile_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            profile_data = json.loads(profile_response.choices[0].message.content)
            
            messages.extend([
                {"role": "assistant", "content": profile_response.choices[0].message.content},
                {"role": "system", "content": CONDITIONS_SYSTEM_PROMPT},
                {"role": "user", "content": "Based on the same paper and the ideal profile you provided, determine the relevancy conditions."}
            ])
            
            # Second call: Get conditions
            conditions_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            
            # Store conditions as text instead of parsing as JSON
            conditions_text = conditions_response.choices[0].message.content
            
            # Add conditions response and request summary
            messages.extend([
                {"role": "assistant", "content": conditions_response.choices[0].message.content},
                {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": "Based on the same paper, provide a summary."}
            ])
            
            # Third call: Get summary
            summary_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            
            summary = summary_response.choices[0].message.content
            
            return {
                "ideal_profile": profile_data,
                "conditions": conditions_text,
                "summary": summary
            }
            
        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")
            raise

    def save_analysis(self, paper_name: str, analysis: Dict) -> None:
        """Save the analysis results to separate directories."""
        print(analysis)
        # Save matching data (profile and conditions)
        matching_dir = Path("data/papers/matching")
        matching_dir.mkdir(exist_ok=True, parents=True)
        matching_data = {
            "ideal_profile": analysis["ideal_profile"],
            "conditions": analysis["conditions"]
        }
        with open(matching_dir / f"{paper_name}.json", 'w') as f:
            json.dump(matching_data, f, indent=2)
        
        # Save summary
        summaries_dir = Path("data/papers/summaries")
        summaries_dir.mkdir(exist_ok=True, parents=True)
        with open(summaries_dir / f"{paper_name}.txt", 'w') as f:
            f.write(analysis["summary"])
