import os
from pathlib import Path
from typing import Optional, List, Dict
import PyPDF2
import tempfile

class PaperProcessor:
    def __init__(self, papers_dir: str = "data/papers/raw"):
        self.papers_dir = Path(papers_dir)
        self.temp_dir = Path("data/papers/text")
        if not self.papers_dir.exists():
            raise FileNotFoundError(f"Papers directory not found: {papers_dir}")
        # Create temp directory if it doesn't exist
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def get_unprocessed_papers(self) -> List[str]:
        """
        Get list of PDF files that haven't been processed yet.
        A paper is considered processed if it exists in the analyzed directory.
        """
        # Get all PDF files from raw directory
        pdf_files = [f.name for f in self.papers_dir.glob("*.pdf")]
        
        # Check which ones have already been analyzed
        analyzed_dir = Path("data/papers/analyzed")
        if analyzed_dir.exists():
            analyzed_files = {f.stem.replace('_analysis', '') for f in analyzed_dir.glob("*_analysis.json")}
            # Return only files that haven't been analyzed
            return [pdf for pdf in pdf_files if Path(pdf).stem not in analyzed_files]
        
        return pdf_files

    def extract_text_from_pdf(self, filename: str) -> Optional[str]:
        """
        Extract text from a PDF file and save to temporary text file.
        
        Args:
            filename: Name of the PDF file (e.g., 'P1.pdf')
            
        Returns:
            str: Extracted text from the PDF, or None if extraction fails
        """
        filepath = self.papers_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"PDF file not found: {filepath}")
            
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                # Save to temporary text file
                temp_path = self.temp_dir / f"{Path(filename).stem}.txt"
                with open(temp_path, 'w', encoding='utf-8') as temp_file:
                    temp_file.write(text)
                
                return text.strip()
                
        except Exception as e:
            print(f"Error processing PDF {filename}: {str(e)}")
            return None

    def process_all_papers(self) -> Dict[str, Optional[str]]:
        """
        Process all unprocessed PDF files in the raw directory.
        
        Returns:
            Dict mapping filename to extracted text (or None if extraction failed)
        """
        results = {}
        unprocessed = self.get_unprocessed_papers()
        
        if not unprocessed:
            print("No new papers to process.")
            return results

        print(f"Found {len(unprocessed)} unprocessed papers.")
        for filename in unprocessed:
            print(f"Processing {filename}...")
            try:
                text = self.extract_text_from_pdf(filename)
                results[filename] = text
                if text:
                    print(f"Successfully processed {filename}")
                else:
                    print(f"Failed to extract text from {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                results[filename] = None
                
        return results

    def cleanup_temp_files(self):
        """Clean up temporary text files after processing."""
        for txt_file in self.temp_dir.glob("*.txt"):
            try:
                txt_file.unlink()
            except Exception as e:
                print(f"Error deleting temporary file {txt_file}: {str(e)}")

def main():
    processor = PaperProcessor()
    try:
        results = processor.process_all_papers()
        
        # Print summary
        print("\nProcessing Summary:")
        print("-" * 50)
        successful = sum(1 for text in results.values() if text is not None)
        print(f"Total papers processed: {len(results)}")
        print(f"Successfully processed: {successful}")
        print(f"Failed to process: {len(results) - successful}")
        
        # Print first 500 chars of first successful extraction as sample
        if successful > 0:
            first_success = next(text for text in results.values() if text is not None)
            print("\nSample of extracted text:")
            print("-" * 50)
            print(first_success[:500])
            
    except Exception as e:
        print(f"Error during batch processing: {str(e)}")
    #finally:
        # Uncomment the following line if to clean up temp files after processing
        # processor.cleanup_temp_files()

if __name__ == "__main__":
    main()
