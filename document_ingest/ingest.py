import os
import gitingest
from urllib.parse import urlparse

def get_repo_name(repo_url):
    """Extract repository name from GitHub URL"""
    path = urlparse(repo_url).path
    return path.strip('/').split('/')[-1].replace('.git', '')

def ingest_repo(repo_url):
    """Ingest a GitHub repository and save its summary, tree, and content"""
    # Create ingested directory if it doesn't exist
    os.makedirs('document_ingest/ingested', exist_ok=True)
    
    # Get repository name
    repo_name = get_repo_name(repo_url)
    
    # Analyze repository
    summary, tree, content = gitingest.ingest(repo_url)
    
    # Create output file
    output_file = os.path.join('document_ingest/ingested', f'{repo_name}.md')
    
    # Write content to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(f'# SDK: {repo_name}\n\n')
        
        f.write('# Summary\n')
        f.write(summary)
        f.write('\n\n')
        
        f.write('# Tree\n')
        f.write(tree)
        f.write('\n\n')
        
        f.write('# Content\n')
        f.write(content)
        f.write('\n')
        f.write('---\n')
    
    print(f"Repository {repo_name} has been successfully ingested to {output_file}") 