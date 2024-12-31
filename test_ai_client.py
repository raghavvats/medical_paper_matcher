from pathlib import Path
from src.ai.openai_client import OpenAIClient

def main():
    # Initialize the client (make sure you have OPENAI_API_KEY in your environment variables)
    client = OpenAIClient()
    paper_to_test = 8
    
    paper_text = Path(f"data/papers/text/P{paper_to_test}.txt").read_text()
    
    # Analyze the paper
    try:
        analysis = client.analyze_paper(paper_text)
        
        client.save_analysis(f"P{paper_to_test}", analysis)
        print(f"\nAnalysis saved to data/papers/processed/P{paper_to_test}_analysis.json")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    import json
    main()