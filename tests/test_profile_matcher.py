from src.core.profile_matcher import ProfileMatcher
import os

def main():
    matcher = ProfileMatcher()
    
    # Get all profiles from data/profiles directory
    profile_dir = os.path.join('data', 'profiles')
    profiles = [f.replace('.json', '') for f in os.listdir(profile_dir) 
                if f.endswith('.json')]
    
    print(f"Found {len(profiles)} profiles to test")
    
    # Test each profile against papers
    for profile_id in profiles:
        print(f"\nTesting profile: {profile_id}")
        matches = matcher.match_profile_to_papers(profile_id)
        
        if matches:
            print(f"Found {len(matches)} matching papers:")
            for paper_id, summary in matches:
                print(f"\nPaper ID: {paper_id}")
                print("Summary:")
                print(summary)
        else:
            print("No matching papers found")
            
        print("-" * 50)

if __name__ == "__main__":
    main()
