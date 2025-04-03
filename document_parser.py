import os
import shutil
import subprocess
from typing import List, Set

class DocumentParser:
    def __init__(
        self,
        repo_url: str,
        included_dirs: List[str],
        excluded_dirs: List[str] = None
    ):
        self.repo_url = repo_url
        self.repo_name = repo_url.split('/')[-1].replace('.git', '')
        self.repo_path = os.path.abspath(self.repo_name)
        self.included_dirs = included_dirs
        self.excluded_dirs = excluded_dirs or []
        self.processed_files: Set[str] = set()
        self.combined_content = []

    def clone_repository(self):
        """Clone the repository if it doesn't exist."""
        if not os.path.exists(self.repo_path):
            try:
                subprocess.run(['git', 'clone', self.repo_url], check=True)
                print(f"Successfully cloned repository from {self.repo_url}")
            except subprocess.CalledProcessError as e:
                print(f"Error cloning repository: {str(e)}")
                raise

    def cleanup(self):
        """Remove the cloned repository after processing."""
        try:
            if os.path.exists(self.repo_path):
                shutil.rmtree(self.repo_path)
                print(f"Cleaned up repository at {self.repo_path}")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def should_process_file(self, file_path: str) -> bool:
        """Check if a file should be processed based on included/excluded directories."""
        rel_path = os.path.relpath(file_path, self.repo_path)
        
        for excluded_dir in self.excluded_dirs:
            if rel_path.startswith(excluded_dir):
                return False
        
        for included_dir in self.included_dirs:
            if rel_path.startswith(included_dir):
                return True
        
        return False

    def process_file(self, file_path: str):
        """Process a single markdown file and extract its content."""
        if file_path in self.processed_files:
            return
        
        self.processed_files.add(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rel_path = os.path.relpath(file_path, self.repo_path)
            self.combined_content.append(f"# {rel_path}\n\n")
            self.combined_content.append(content)
            self.combined_content.append("\n---\n\n")
            
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

    def process_directory(self, directory: str):
        """Process all markdown files in a directory recursively."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    if self.should_process_file(file_path):
                        self.process_file(file_path)

    def generate_combined_document(self, output_file: str):
        """Generate the combined documentation file."""
        try:
            self.clone_repository()
            self.process_directory(self.repo_path)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(self.combined_content)
            
            print(f"Successfully generated combined documentation at {output_file}")
            
        finally:
            self.cleanup()

def main():
    parser = DocumentParser(
        repo_url="https://github.com/LikeMindsCommunity/likeminds-docs.git",
        included_dirs=["feed/Android"],
        excluded_dirs=["feed/Android/Data"]
    )
    
    parser.generate_combined_document("combined_documentation.md")

if __name__ == "__main__":
    main() 