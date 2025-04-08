"""
Core document parsing functionality.
"""

import os
import shutil
import subprocess
from typing import List, Set
import requests
from urllib.parse import urlparse
import re
from code_generator.config import Settings

class DocumentParser:
    def __init__(self, settings: Settings = None):
        """
        Initialize the document parser with settings.
        
        Args:
            settings (Settings, optional): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.repo_name = self.settings.repo_url.split('/')[-1].replace('.git', '')
        self.repo_path = os.path.abspath(self.repo_name)
        self.processed_files: Set[str] = set()
        self.combined_content = []
        self.github_files = {}  # Store GitHub file content and their IDs

    def clone_repository(self):
        """Clone the repository if it doesn't exist."""
        if not os.path.exists(self.repo_path):
            try:
                subprocess.run(['git', 'clone', self.settings.repo_url], check=True)
                print(f"Successfully cloned repository from {self.settings.repo_url}")
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
        
        for excluded_dir in self.settings.excluded_dirs:
            if excluded_dir and rel_path.startswith(excluded_dir):
                return False
        
        for included_dir in self.settings.included_dirs:
            if included_dir and rel_path.startswith(included_dir):
                return True
        
        return False

    def extract_headings(self, content: str) -> List[str]:
        """Extract headings from markdown content."""
        headings = []
        for line in content.split('\n'):
            if line.startswith('#'):
                headings.append(line)
        return headings

    def process_file(self, file_path: str):
        """Process a single markdown file and extract its content."""
        if file_path in self.processed_files:
            return
        
        self.processed_files.add(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract and convert headings to subheadings
            headings = self.extract_headings(content)
            
            # Add file path as a heading
            rel_path = os.path.relpath(file_path, self.repo_path)
            self.combined_content.append(f"# {rel_path}\n\n")
            
            # Add subheadings summary
            if headings:
                self.combined_content.append("## Subheadings in this file:\n")
                for heading in headings:
                    # Extract the text part of the heading for the summary
                    heading_text = heading.lstrip('#').strip()
                    self.combined_content.append(f"- {heading_text}\n")
                self.combined_content.append("\n")
            
            # Process content to convert headings to subheadings and links
            processed_content = []
            for line in content.split('\n'):
                if line.startswith('#'):
                    # Convert to subheading by adding one more #
                    level = len(line) - len(line.lstrip('#'))
                    heading_text = line.lstrip('#').strip()
                    processed_content.append(f"{'#' * (level + 1)} {heading_text}")
                else:
                    # Convert relative links to IDs and handle GitHub links
                    processed_line = self.convert_relative_links_to_ids(line)
                    processed_content.append(processed_line)
            
            # Add the processed content
            self.combined_content.append('\n'.join(processed_content))
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

    def generate_combined_document(self):
        """Generate the combined documentation file."""
        try:
            self.clone_repository()
            self.process_directory(self.repo_path)
            self.save_combined_documentation()
            print(f"Successfully generated combined documentation at {self.settings.output_file}")
        finally:
            self.cleanup()

    def fetch_github_raw_content(self, github_url: str) -> str:
        """Fetch raw content from a GitHub URL."""
        # Convert GitHub URL to raw content URL
        parsed_url = urlparse(github_url)
        if 'github.com' not in parsed_url.netloc:
            return ""
            
        # Convert to raw content URL
        path_parts = parsed_url.path.split('/')
        if len(path_parts) < 5:  # Need at least owner/repo/blob/branch/path
            return ""
            
        # Remove 'blob' from path
        if 'blob' in path_parts:
            path_parts.remove('blob')
            
        # Reconstruct raw URL
        raw_url = f"https://raw.githubusercontent.com/{'/'.join(path_parts[1:])}"
        
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching GitHub content from {raw_url}: {str(e)}")
            return ""

    def convert_relative_links_to_ids(self, content: str) -> str:
        """Convert relative path links to absolute IDs in markdown content."""
        # Pattern to match markdown links with relative paths
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Handle GitHub links
            if 'github.com' in link_path and '/blob/' in link_path:
                # Generate a unique ID for this GitHub file
                file_id = f"github-{len(self.github_files)}"
                # Fetch and store the content
                raw_content = self.fetch_github_raw_content(link_path)
                if raw_content:
                    self.github_files[file_id] = {
                        'content': raw_content,
                        'title': link_text,
                        'url': link_path
                    }
                # Keep the original link
                return match.group(0)
            
            # Keep all other links unchanged
            return match.group(0)
        
        # Replace all relative links in the content
        return re.sub(pattern, replace_link, content)

    def save_combined_documentation(self):
        """Save the combined documentation to a file."""
        with open(self.settings.output_file, 'w', encoding='utf-8') as f:
            # Write main content
            f.write(''.join(self.combined_content))
            
            # Add GitHub files content at the end if any exist
            if self.github_files:
                f.write("\n# GitHub Files\n\n")
                for file_id, file_data in self.github_files.items():
                    f.write(f"## {file_data['title']}\n\n")
                    f.write(f"Source: [{file_data['url']}]({file_data['url']})\n\n")
                    f.write("```kotlin\n")
                    f.write(file_data['content'])
                    f.write("\n```\n\n")
                    f.write("---\n\n") 