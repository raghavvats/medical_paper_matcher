import json
import os
from typing import Dict, List, Optional, Tuple

from src.core.condition_parser import ConditionParser

class ProfileMatcher:
    def __init__(self):
        self.condition_parser = ConditionParser()
        
    def match_profile_to_papers(self, profile_id: str) -> List[Tuple[str, str]]:
        """
        Match a profile against all available papers and return matching papers with their summaries.
        
        Args:
            profile_id: ID of the profile to match
            
        Returns:
            List of tuples containing (paper_id, paper_summary) for matching papers
        """
        profile = self._load_profile(profile_id)
        if not profile:
            return []
            
        matches = []
        for paper_id, paper_data in self._load_papers():
            if self._is_match(profile, paper_data):
                summary = self._get_paper_summary(paper_id)
                if summary:
                    matches.append((paper_id, summary))
                    
        return matches
    
    def _load_profile(self, profile_id: str) -> Optional[Dict]:
        """
        Load a profile from the profiles directory.
        
        Args:
            profile_id: ID of the profile to load
            
        Returns:
            Dictionary containing profile data or None if not found
        """
        profile_path = os.path.join('data', 'profiles', f'{profile_id}.json')
        try:
            with open(profile_path, 'r') as f:
                return json.load(f)  # Return the nested structure as-is
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def _load_papers(self) -> List[Tuple[str, Dict]]:
        """
        Load all papers from the matching directory.
        
        Returns:
            List of tuples containing (paper_id, paper_data)
        """
        papers = []
        matching_dir = os.path.join('data', 'papers', 'matching')
        
        for filename in os.listdir(matching_dir):
            if filename.endswith('.json'):
                paper_id = filename.replace('.json', '')
                paper_path = os.path.join(matching_dir, filename)
                
                try:
                    with open(paper_path, 'r') as f:
                        paper_data = json.load(f)
                        papers.append((paper_id, paper_data))
                except (FileNotFoundError, json.JSONDecodeError):
                    continue
                    
        return papers
    
    def _is_match(self, profile: Dict, paper_data: Dict) -> bool:
        """
        Check if a profile matches the conditions specified in a paper.
        
        Args:
            profile: Dictionary containing profile characteristics
            paper_data: Dictionary containing paper data including conditions
            
        Returns:
            bool: True if profile matches paper conditions, False otherwise
        """
        print(f"Checking match with profile: {profile}")
        print(f"Against paper data: {paper_data}")
        
        if 'conditions' not in paper_data or 'ideal_profile' not in paper_data:
            print("Missing conditions or ideal_profile in paper data")
            return False
            
        # Remove quotes from conditions if present
        conditions = paper_data['conditions'].strip('"')
        print(f"Evaluating conditions: {conditions}")
        
        result = self.condition_parser.parse_conditions(
            conditions,
            profile,
            paper_data['ideal_profile']
        )
        print(f"Match result: {result}")
        return result
    
    def _get_paper_summary(self, paper_id: str) -> Optional[str]:
        """
        Retrieve the summary for a given paper.
        
        Args:
            paper_id: ID of the paper to get summary for
            
        Returns:
            String containing paper summary or None if not found
        """
        summary_path = os.path.join('data', 'papers', 'summaries', f'{paper_id}.txt')
        try:
            with open(summary_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
