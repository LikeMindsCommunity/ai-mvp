import os
import gitingest
from urllib.parse import urlparse
import subprocess
import shutil

def get_repo_name(repo_url):
    """Extract repository name from GitHub URL"""
    path = urlparse(repo_url).path
    return path.strip('/').split('/')[-1].replace('.git', '')

def clone_repo(repo_url, repo_name):
    """Clone a repository into the private_repo directory"""
    private_repo_dir = os.path.join('document_ingest', 'private_repo', repo_name)
    os.makedirs(os.path.dirname(private_repo_dir), exist_ok=True)
    
    # Remove existing directory if it exists
    if os.path.exists(private_repo_dir):
        shutil.rmtree(private_repo_dir)
    
    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, private_repo_dir], check=True)
    return private_repo_dir

def filter_directories(repo_path, include_dirs=None, exclude_dirs=None):
    """Filter repository contents based on include/exclude directories"""
    if not include_dirs and not exclude_dirs:
        return
    
    # Convert to absolute paths
    if include_dirs:
        include_dirs = [os.path.join(repo_path, d) for d in include_dirs]
    if exclude_dirs:
        exclude_dirs = [os.path.join(repo_path, d) for d in exclude_dirs]
    
    # First handle includes
    if include_dirs:
        # Create a temporary directory to store the filtered content
        temp_dir = os.path.join(repo_path, 'temp_filtered')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Copy included directories to temp directory
        for include_dir in include_dirs:
            if os.path.exists(include_dir):
                rel_path = os.path.relpath(include_dir, repo_path)
                dest_path = os.path.join(temp_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if os.path.isfile(include_dir):
                    shutil.copy2(include_dir, dest_path)
                else:
                    shutil.copytree(include_dir, dest_path, dirs_exist_ok=True)
        
        # Remove original content and move filtered content back
        for item in os.listdir(repo_path):
            if item != 'temp_filtered':
                item_path = os.path.join(repo_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path)
        
        # Move filtered content back to repo_path
        for item in os.listdir(temp_dir):
            shutil.move(os.path.join(temp_dir, item), repo_path)
        
        # Remove temp directory
        shutil.rmtree(temp_dir)
    
    # Then handle excludes
    if exclude_dirs:
        for exclude_dir in exclude_dirs:
            if os.path.exists(exclude_dir):
                if os.path.isfile(exclude_dir):
                    os.remove(exclude_dir)
                else:
                    shutil.rmtree(exclude_dir)

def ingest_repo(repo_url, is_private=False, include_dirs=None, exclude_dirs=None, private_repo_name=None):
    """Ingest a GitHub repository and save its summary, tree, and content"""
    # Create ingested directory if it doesn't exist
    os.makedirs('document_ingest/ingested', exist_ok=True)
    
    # Get repository name from argument or URL
    if private_repo_name is None:
        private_repo_name = get_repo_name(repo_url)
    
    # Always clone if include/exclude directories are specified
    if include_dirs or exclude_dirs or is_private:
        repo_path = clone_repo(repo_url, private_repo_name)
        if include_dirs or exclude_dirs:
            filter_directories(repo_path, include_dirs, exclude_dirs)
        summary, tree, content = gitingest.ingest(repo_path)
    else:
        summary, tree, content = gitingest.ingest(repo_url)
    
    # Create output file
    output_file = os.path.join('document_ingest/ingested', f'{private_repo_name}.md')
    
    # Write content to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(f'# SDK: {private_repo_name}\n\n')
        
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
    
    print(f"Repository {private_repo_name} has been successfully ingested to {output_file}") 