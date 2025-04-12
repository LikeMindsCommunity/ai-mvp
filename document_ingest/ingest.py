import os
import gitingest
from urllib.parse import urlparse
import subprocess
import shutil

def get_repo_name(repo_url):
    """Extract repository name from GitHub URL"""
    path = urlparse(repo_url).path
    return path.strip('/').split('/')[-1].replace('.git', '')

def clone_private_repo(repo_url, repo_name):
    """Clone a private repository into the private_repo directory"""
    private_repo_dir = os.path.join('document_ingest', 'private_repo', repo_name)
    os.makedirs(os.path.dirname(private_repo_dir), exist_ok=True)
    
    # Remove existing directory if it exists
    if os.path.exists(private_repo_dir):
        shutil.rmtree(private_repo_dir)
    
    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, private_repo_dir], check=True)
    return private_repo_dir

def ingest_repo(repo_url, is_private=False):
    """Ingest a GitHub repository and save its summary, tree, and content"""
    # Create ingested directory if it doesn't exist
    os.makedirs('document_ingest/ingested', exist_ok=True)
    
    # Get repository name
    repo_name = get_repo_name(repo_url)
    
    # Handle private repositories
    if is_private:
        repo_path = clone_private_repo(repo_url, repo_name)
        summary, tree, content = gitingest.ingest(repo_path)
    else:
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