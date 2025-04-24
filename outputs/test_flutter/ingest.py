import os
import asyncio
from urllib.parse import urlparse
import shutil
from pathlib import Path

def get_repo_name(path_or_url):
    """Extract the repository name from a path or URL."""
    return os.path.basename(os.path.normpath(path_or_url))

def generate_tree(directory, exclude_dirs):
    """Generate a tree structure of the given directory, excluding specified directories."""
    tree = []
    for root, dirs, files in os.walk(directory):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if not any(d.startswith(exclude) for exclude in exclude_dirs)]
        level = root.replace(directory, '').count(os.sep)
        indent = '    ' * level
        tree.append(f"{indent}└── {os.path.basename(root)}/")
        sub_indent = '    ' * (level + 1)
        for file in files:
            tree.append(f"{sub_indent}{file}")
    return '\n'.join(tree)

async def ingest_repo(repo_path_or_url: str, include_dirs: list = None, exclude_dirs: list = None) -> tuple[str, str, str]:
    """
    Ingest a local directory and save its summary, tree, and content.

    Args:
        repo_path_or_url (str): Path to local directory
        include_dirs (list): List of directories to include
        exclude_dirs (list): List of directories to exclude

    Returns:
        tuple[str, str, str]: (summary, tree, content)
    """
    print(f"\n=== Starting ingest_repo ===")
    print(f"Input parameters:")
    print(f"- repo_path_or_url: {repo_path_or_url}")
    print(f"- include_dirs: {include_dirs}")
    print(f"- exclude_dirs: {exclude_dirs}")

    # Create ingested directory if it doesn't exist
    os.makedirs('document_ingest/ingested', exist_ok=True)

    repo_name = get_repo_name(repo_path_or_url)
    print(f"- repo_name: {repo_name}")

    try:
        # Generate summary, tree, and content
        print("Generating project summary...")
        total_files = sum(len(files) for _, dirs, files in os.walk(repo_path_or_url) if not any(d.startswith(tuple(exclude_dirs)) for d in dirs))
        summary = f"Directory: {repo_path_or_url}\nFiles analyzed: {total_files}\n"

        print("Generating project tree...")
        tree = generate_tree(repo_path_or_url, exclude_dirs)

        print("Reading content of specific files...")
        content = ""
        if include_dirs:
            for dir_name in include_dirs:
                dir_path = os.path.join(repo_path_or_url, dir_name)
                if os.path.exists(dir_path):
                    for root, dirs, files in os.walk(dir_path):
                        # Exclude specified directories
                        dirs[:] = [d for d in dirs if not any(d.startswith(exclude) for exclude in exclude_dirs)]
                        for file in files:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content += f"\n---\n# {file}\n" + f.read()

        # Add content from pubspec.yaml
        pubspec_path = os.path.join(repo_path_or_url, 'pubspec.yaml')
        if os.path.exists(pubspec_path):
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                content += f"\n---\n# pubspec.yaml\n" + f.read()

        # Write content to file
        output_file = os.path.join('document_ingest/ingested', f'{os.path.basename(repo_path_or_url)}.md')
        print(f"\n- output_file: {output_file}")

        print("Writing content to file...")
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

        print(f"\nRepository {repo_name} has been successfully ingested to {output_file}")
        print("=== End of ingest_repo ===\n")
        return summary, tree, content

    except Exception as e:
        print(f"\nERROR in ingest_repo: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    asyncio.run(ingest_repo(".", include_dirs=["lib"], exclude_dirs=[".", "android", "ios", "web", "macos", "build"]))