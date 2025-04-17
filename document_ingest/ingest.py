import os
import gitingest
from urllib.parse import urlparse
import subprocess
import shutil
import asyncio

def get_repo_name(repo_url):
    """Extract repository name from GitHub URL"""
    print(f"\n=== Starting get_repo_name ===")
    print(f"Input repo_url: {repo_url}")
    
    try:
        path = urlparse(repo_url).path
        repo_name = path.strip('/').split('/')[-1].replace('.git', '')
        print(f"Extracted repo_name: {repo_name}")
        print("=== End of get_repo_name ===\n")
        return repo_name
    except Exception as e:
        print(f"\nERROR in get_repo_name: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        print("=== End of get_repo_name with error ===\n")
        raise

async def clone_repo(repo_url, repo_name):
    """Clone a repository into the private_repo directory"""
    print(f"\n=== Starting clone_repo ===")
    print(f"Input parameters:")
    print(f"- repo_url: {repo_url}")
    print(f"- repo_name: {repo_name}")
    
    try:
        private_repo_dir = os.path.join('document_ingest', 'private_repo', repo_name)
        print(f"Target directory: {private_repo_dir}")
        
        os.makedirs(os.path.dirname(private_repo_dir), exist_ok=True)
        
        # Remove existing directory if it exists
        if os.path.exists(private_repo_dir):
            print(f"Removing existing directory: {private_repo_dir}")
            shutil.rmtree(private_repo_dir)
        
        # Clone the repository
        print("Starting git clone...")
        process = await asyncio.create_subprocess_exec(
            'git', 'clone', repo_url, private_repo_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"\nGit clone failed with return code: {process.returncode}")
            print(f"stderr: {stderr.decode()}")
            raise Exception(f"Git clone failed: {stderr.decode()}")
        
        print(f"Successfully cloned repository to: {private_repo_dir}")
        print("=== End of clone_repo ===\n")
        return private_repo_dir
        
    except Exception as e:
        print(f"\nERROR in clone_repo: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        print("=== End of clone_repo with error ===\n")
        raise

async def create_local_repo(source_path: str, repo_name: str) -> str:
    """
    Create a temporary local repository from a source directory.
    
    Args:
        source_path (str): Path to the source directory
        repo_name (str): Name for the repository
        
    Returns:
        str: Path to the created local repository
    """
    print(f"\n=== Starting create_local_repo ===")
    print(f"Input parameters:")
    print(f"- source_path: {source_path}")
    print(f"- repo_name: {repo_name}")
    
    try:
        local_repo_dir = os.path.join('document_ingest', 'local_repo', repo_name)
        print(f"Target directory: {local_repo_dir}")
        
        os.makedirs(os.path.dirname(local_repo_dir), exist_ok=True)
        
        # Remove existing directory if it exists
        if os.path.exists(local_repo_dir):
            print(f"Removing existing directory: {local_repo_dir}")
            shutil.rmtree(local_repo_dir)
        
        # Copy the source directory to local repo directory
        print(f"Copying from {source_path} to {local_repo_dir}")
        await asyncio.to_thread(shutil.copytree, source_path, local_repo_dir)
        
        print(f"Successfully created local repository at: {local_repo_dir}")
        print("=== End of create_local_repo ===\n")
        return local_repo_dir
        
    except Exception as e:
        print(f"\nERROR in create_local_repo: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        print("=== End of create_local_repo with error ===\n")
        raise

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

async def ingest_repo(repo_path_or_url: str, is_private: bool = False, include_dirs: list = None, exclude_dirs: list = None, private_repo_name: str = None) -> tuple[str, str, str, str]:
    """
    Ingest a GitHub repository or local directory and save its summary, tree, and content.
    
    Args:
        repo_path_or_url (str): Path to local directory or URL of GitHub repository
        is_private (bool): Whether the repository is private
        include_dirs (list): List of directories to include
        exclude_dirs (list): List of directories to exclude
        private_repo_name (str): Custom name for the repository (optional)
        
    Returns:
        tuple[str, str, str, str]: (summary, tree, content, output_file_path)
    """
    print(f"\n=== Starting ingest_repo ===")
    print(f"Input parameters:")
    print(f"- repo_path_or_url: {repo_path_or_url}")
    print(f"- is_private: {is_private}")
    print(f"- include_dirs: {include_dirs}")
    print(f"- exclude_dirs: {exclude_dirs}")
    print(f"- private_repo_name: {private_repo_name}")
    
    # Create ingested directory if it doesn't exist
    os.makedirs('document_ingest/ingested', exist_ok=True)
    
    # Determine if the input is a URL or local path
    is_url = bool(urlparse(repo_path_or_url).scheme)
    print(f"\n- is_url: {is_url}")
    
    # Initialize variables
    repo_name = private_repo_name
    repo_path = None
    
    # Determine repository name if not provided
    if repo_name is None:
        repo_name = get_repo_name(repo_path_or_url) if is_url else os.path.basename(os.path.normpath(repo_path_or_url))
    print(f"- repo_name: {repo_name}")
    
    try:
        # Handle URL case
        if is_url:
            print("\nHandling URL case...")
            if include_dirs or exclude_dirs or is_private:
                print("Cloning repository...")
                # Clone the repository
                repo_path = await clone_repo(repo_path_or_url, repo_name)
                print(f"- repo_path after clone: {repo_path}")
                
                # Apply filters
                if include_dirs or exclude_dirs:
                    print("Applying filters...")
                    await asyncio.to_thread(filter_directories, repo_path, include_dirs, exclude_dirs)
                
                # Get content from cloned repository
                print("Getting content from cloned repository...")
                summary, tree, content = await asyncio.to_thread(gitingest.ingest, repo_path)
            else:
                print("Getting content directly from URL...")
                # Get content directly from URL
                summary, tree, content = await asyncio.to_thread(gitingest.ingest, repo_path_or_url)
        
        # Handle local path case
        else:
            print("\nHandling local path case...")
            if include_dirs or exclude_dirs:
                print("Creating local repository copy...")
                # Create a local repository copy
                repo_path = await create_local_repo(repo_path_or_url, repo_name)
                print(f"- repo_path after local copy: {repo_path}")
                
                # Apply filters
                print("Applying filters...")
                await asyncio.to_thread(filter_directories, repo_path, include_dirs, exclude_dirs)
                
                # Get content from local repository
                print("Getting content from local repository...")
                summary, tree, content = await asyncio.to_thread(gitingest.ingest, repo_path)
            else:
                print("Getting content directly from local path...")
                # Get content directly from local path
                summary, tree, content = await asyncio.to_thread(gitingest.ingest, repo_path_or_url)
        
        # Create output file
        output_file = os.path.join('document_ingest/ingested', f'{repo_name}.md')
        print(f"\n- output_file: {output_file}")
        
        # Write content to file
        print("Writing content to file...")
        def write_file():
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
        
        await asyncio.to_thread(write_file)
        
        print(f"\nRepository {repo_name} has been successfully ingested to {output_file}")
        print("=== End of ingest_repo ===\n")
        return summary, tree, content, output_file
        
    except Exception as e:
        print(f"\nERROR in ingest_repo: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        print("=== End of ingest_repo with error ===\n")
        raise
        
    finally:
        # Clean up any temporary repositories
        if repo_path and os.path.exists(repo_path):
            print(f"\nCleaning up temporary repository at: {repo_path}")
            await asyncio.to_thread(shutil.rmtree, repo_path) 