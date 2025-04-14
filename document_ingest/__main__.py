import sys
import os
import argparse
from .ingest import ingest_repo

def main():
    parser = argparse.ArgumentParser(description='Ingest a GitHub repository')
    parser.add_argument('repo_url', help='GitHub repository URL')
    parser.add_argument('--private', action='store_true', help='Repository is private')
    parser.add_argument('--include', nargs='+', help='Directories to include')
    parser.add_argument('--exclude', nargs='+', help='Directories to exclude')
    parser.add_argument('--private-repo-name', help='Custom name for the private repository (optional)')
    
    args = parser.parse_args()
    
    try:
        ingest_repo(
            args.repo_url,
            is_private=args.private,
            include_dirs=args.include,
            exclude_dirs=args.exclude,
            repo_name=args.private_repo_name
        )
    except Exception as e:
        print(f"Error ingesting repository: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 