import sys
import os
from .ingest import ingest_repo

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m document_ingest <github_repo_url> [--private]")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    is_private = '--private' in sys.argv
    
    try:
        ingest_repo(repo_url, is_private=is_private)
    except Exception as e:
        print(f"Error ingesting repository: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 