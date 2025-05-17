import os
import json
import click
from rich.console import Console
from rich.prompt import Prompt
from google import genai
from google.genai import types
import subprocess
import requests

# Constants
SESSION_DIR = ".multiagent_cli_sessions"
GEMINI_API_KEY = "AIzaSyAe4CWfuUbYWbOk0UY0DfKn8H5DRkPfpMM"
GEMINI_MODEL = "gemini-2.5-pro-preview-05-06"
DOCS_URLS = {
    'hawcx': "https://docs.hawcx.com/llms-full.txt"
}

console = Console()

# Ensure session directory exists
def ensure_session_dir():
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

# Session management
def load_session(session_name):
    path = os.path.join(SESSION_DIR, f"{session_name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_session(session_name, data):
    path = os.path.join(SESSION_DIR, f"{session_name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Agent base class
class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def act(self, context, user_input, session_data):
        raise NotImplementedError

# Query Analyzer Agent
class QueryAnalyzer(Agent):
    def __init__(self):
        super().__init__("QueryAnalyzer", "Analyzes user query and extracts requirements.")

    def act(self, context, user_input, session_data):
        client = get_gemini_client()
        prompt = f"Analyze the following user request and extract the main features and requirements for a JavaScript app.\nRequest: {user_input}"
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        session_data['requirements'] = response.text
        console.print(f"[bold magenta]Requirements:[/bold magenta]\n{response.text}")
        return session_data

# Project Scaffolder Agent
class ProjectScaffolder(Agent):
    def __init__(self):
        super().__init__("ProjectScaffolder", "Creates project directory structure.")

    def act(self, context, user_input, session_data):
        project_name = session_data.get('project_name') or Prompt.ask("Enter a name for your JS project", default="my-js-app")
        session_data['project_name'] = project_name
        
        # Create generated_projects directory if it doesn't exist
        generated_projects_dir = "generated_projects"
        if not os.path.exists(generated_projects_dir):
            os.makedirs(generated_projects_dir)
        
        project_dir = os.path.abspath(os.path.join(generated_projects_dir, project_name))
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            console.print(f"[green]Project directory created at {project_dir}[/green]")
        else:
            console.print(f"[yellow]Project directory already exists at {project_dir}[/yellow]")
        
        session_data['project_dir'] = project_dir
        return session_data

# Feature Implementer Agent
class FeatureImplementer(Agent):
    def __init__(self):
        super().__init__("FeatureImplementer", "Implements features and generates all project files.")

    def act(self, context, user_input, session_data):
        client = get_gemini_client()
        project_dir = session_data.get('project_dir')
        requirements = session_data.get('requirements', '')
        if not project_dir:
            return session_data

        # Check if authentication is needed
        auth_keywords = ['auth', 'login', 'sign in', 'signin', 'authentication', 'passwordless']
        needs_auth = any(keyword in requirements.lower() for keyword in auth_keywords)

        # Get docs URL and API key if authentication is needed
        docs_url = None
        api_key = None
        if needs_auth:
            # Get or prompt for API key
            api_key = session_data.get('api_key') or Prompt.ask("Enter your API Key")
            session_data['api_key'] = api_key
            
            # Get or prompt for docs URL
            docs_url = session_data.get('docs_url')
            if not docs_url:
                docs_url = DOCS_URLS.get('hawcx')  # Default to Hawcx docs if none specified
                session_data['docs_url'] = docs_url

            # Fetch docs if URL is available
            docs_content = None
            if docs_url:
                docs_content = fetch_docs(docs_url)
                if not docs_content:
                    console.print("[yellow]Warning: Could not fetch documentation. Proceeding without it.[/yellow]")

        # Common requirements for both cases
        common_requirements = """
Requirements for the code:
1. Use modern JavaScript (ES6+)
2. Include proper error handling
3. Use async/await for asynchronous operations
4. Follow best practices for DOM manipulation
5. Include comments for complex logic
6. Make the code modular and maintainable
7. Generate all HTML elements dynamically in JavaScript using template literals
8. Use a single root div element in the HTML file
9. Include all necessary CSS classes and styling in the JavaScript
10. Ensure the UI is responsive and user-friendly
11. Use Bootstrap or similar CSS framework for styling
12. Handle all DOM events and state management in JavaScript
13. Include loading states and error messages
14. Use proper form validation and user feedback

Return a JSON array where each object has:
- filename: string (e.g., "main.js", "index.html", "package.json")
- content: string (the actual code/content without any markdown formatting)

JSON Formatting Rules:
1. Use double quotes for all strings (not single quotes)
2. Escape all double quotes in content with backslash (\")
3. Escape all newlines in content with \\n
4. Escape all backslashes in content with double backslash (\\\\)
5. Do not include any comments in the JSON
6. Do not include any trailing commas
7. Do not include any markdown formatting
8. Ensure all content strings are properly escaped
9. Use proper JSON array syntax with square brackets []
10. Use proper JSON object syntax with curly braces {}
11. Each object must be separated by a comma
12. The last object should not have a trailing comma

Example format:
[
    {
        "filename": "index.html",
        "content": "<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>My App</title>\\n</head>\\n<body>\\n    <div id=\\"root\\"></div>\\n</body>\\n</html>"
    },
    {
        "filename": "main.js",
        "content": "// JavaScript code\\nconst app = () => {\\n    console.log(\\"Hello\\");\\n};"
    },
    {
        "filename": "package.json",
        "content": "{\\"name\\": \\"my-app\\",\\"version\\": \\"1.0.0\\"}"
    }
]"""

        # Generate the prompt based on whether authentication is needed
        if needs_auth:
            prompt = f"""Generate a complete JavaScript web application that includes both the requested requirements and authentication (using the API key and documentation). Return a JSON array of files as specified in the requirements.

Requirements: {requirements}

Documentation:
{docs_content if docs_content else 'No documentation available'}

API Key: {api_key}

{common_requirements}"""
        else:
            prompt = f"""Generate a complete JavaScript web application based on the following requirements. Return a JSON array of files as specified in the requirements.

Requirements: {requirements}

{common_requirements}"""

        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        
        # Clean the response text to remove any markdown formatting
        response_text = response.text
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove closing ```
        response_text = response_text.strip()
        
        try:
            # Parse the JSON array of files
            files = json.loads(response_text)
            
            # Write all files to the project directory
            for file in files:
                filename = file['filename']
                content = file['content']
                file_path = os.path.join(project_dir, filename)
                with open(file_path, "w") as f:
                    f.write(content)
                console.print(f"[green]Generated {filename}[/green]")
            
            if needs_auth:
                console.print(f"[green]Features implemented with authentication[/green]")
            else:
                console.print(f"[cyan]Features implemented[/cyan]")
                
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing generated files: {e}[/red]")
        
        return session_data

# Code Explainer Agent
class CodeExplainer(Agent):
    def __init__(self):
        super().__init__("CodeExplainer", "Explains code and generates README with setup instructions.")

    def act(self, context, user_input, session_data):
        project_dir = session_data.get('project_dir')
        if not project_dir:
            return session_data

        # Read all files in the project directory
        files_content = {}
        try:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    # Skip node_modules and other common directories/files
                    if any(skip in root for skip in ['node_modules', '.git', '.vscode']):
                        continue
                    
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            files_content[relative_path] = content
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not read {relative_path}: {str(e)}[/yellow]")

        except Exception as e:
            console.print(f"[red]Error reading project files: {str(e)}[/red]")
            return session_data

        # Generate README content using LLM
        client = get_gemini_client()
        prompt = f"""Generate a comprehensive README.md for a JavaScript project. Include:
1. Project overview
2. Features
3. Setup instructions
4. How to run the project
5. Code structure explanation
6. Authentication flow explanation (if authentication is needed)

Project files content:
{json.dumps(files_content, indent=2)}

Return only the README.md content in markdown format without any additional text or explanations."""
        
        try:
            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            readme_content = response.text

            # Write README.md
            readme_path = os.path.join(project_dir, "README.md")
            with open(readme_path, 'w') as f:
                f.write(readme_content)

            console.print(f"[green]README.md generated with project documentation[/green]")
        except Exception as e:
            console.print(f"[red]Error generating README: {str(e)}[/red]")

        return session_data

# Test Agent
class TestAgent(Agent):
    def __init__(self):
        super().__init__("TestAgent", "Validates and fixes compilation errors in project files.")
        self.ensure_validation_tools()

    def ensure_validation_tools(self):
        """Ensure all required validation tools are installed."""
        tools = {
            'htmlhint': 'npm install -g htmlhint',
            'stylelint': 'npm install -g stylelint stylelint-config-standard'
        }
        
        for tool, install_cmd in tools.items():
            try:
                # Check if tool is installed
                result = subprocess.run(["which", tool], capture_output=True, text=True)
                if result.returncode != 0:
                    console.print(f"[yellow]Installing {tool}...[/yellow]")
                    install_result = subprocess.run(install_cmd.split(), capture_output=True, text=True)
                    if install_result.returncode == 0:
                        console.print(f"[green]Successfully installed {tool}[/green]")
                    else:
                        console.print(f"[red]Failed to install {tool}: {install_result.stderr}[/red]")
            except Exception as e:
                console.print(f"[red]Error checking/installing {tool}: {str(e)}[/red]")

    def validate_js_file(self, file_path):
        """Validate JavaScript file syntax using Node.js."""
        try:
            result = subprocess.run(["node", "--check", file_path], capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr if result.returncode != 0 else None
        except Exception as e:
            return False, str(e)

    def validate_html_file(self, file_path):
        """Validate HTML file using htmlhint."""
        try:
            result = subprocess.run(["htmlhint", file_path], capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr if result.returncode != 0 else None
        except Exception as e:
            return False, str(e)

    def validate_css_file(self, file_path):
        """Validate CSS file using stylelint."""
        try:
            result = subprocess.run(["stylelint", file_path], capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr if result.returncode != 0 else None
        except Exception as e:
            return False, str(e)

    def fix_file_content(self, file_path, error_message, file_content):
        """Use Gemini to fix file content based on error message."""
        try:
            client = get_gemini_client()
            file_type = os.path.splitext(file_path)[1].lower()
            
            prompt = f"""Fix the following {file_type} code that has compilation errors. Return only the fixed code without any explanations.

Error message:
{error_message}

Code to fix:
{file_content}"""

            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            fixed_content = response.text.strip()
            
            return fixed_content
        except Exception as e:
            console.print(f"[red]Error fixing {file_path}: {str(e)}[/red]")
            return None

    def act(self, context, user_input, session_data):
        project_dir = session_data.get('project_dir')
        if not project_dir:
            console.print("[red]No project directory found in session data[/red]")
            return session_data

        # Track validation results
        validation_results = []
        files_fixed = []

        try:
            # Walk through all files in the project directory
            for root, _, files in os.walk(project_dir):
                # Skip node_modules and other common directories
                if any(skip in root for skip in ['node_modules', '.git', '.vscode']):
                    continue

                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_dir)
                    file_ext = os.path.splitext(file)[1].lower()

                    # Skip non-code files
                    if file_ext not in ['.js', '.html', '.css']:
                        continue

                    console.print(f"[cyan]Validating {relative_path}...[/cyan]")
                    
                    # Validate based on file type
                    is_valid = False
                    error_message = None
                    
                    if file_ext == '.js':
                        is_valid, error_message = self.validate_js_file(file_path)
                    elif file_ext == '.html':
                        is_valid, error_message = self.validate_html_file(file_path)
                    elif file_ext == '.css':
                        is_valid, error_message = self.validate_css_file(file_path)

                    if not is_valid:
                        console.print(f"[yellow]Found errors in {relative_path}[/yellow]")
                        console.print(f"[yellow]Error: {error_message}[/yellow]")
                        
                        # Read file content
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                            
                            # Get fixed content
                            fixed_content = self.fix_file_content(file_path, error_message, file_content)
                            
                            if fixed_content:
                                # Write the fixed content
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(fixed_content)
                                
                                # Re-validate the file
                                is_valid = False
                                if file_ext == '.js':
                                    is_valid, _ = self.validate_js_file(file_path)
                                elif file_ext == '.html':
                                    is_valid, _ = self.validate_html_file(file_path)
                                elif file_ext == '.css':
                                    is_valid, _ = self.validate_css_file(file_path)
                                
                                if is_valid:
                                    console.print(f"[green]Fixed {relative_path}[/green]")
                                    files_fixed.append(relative_path)
                                else:
                                    console.print(f"[red]Fix attempt failed for {relative_path}[/red]")
                                    # Revert to original content if fix didn't work
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(file_content)
                        except Exception as e:
                            console.print(f"[red]Error processing {relative_path}: {str(e)}[/red]")
                    
                    validation_results.append((relative_path, is_valid))

        except Exception as e:
            console.print(f"[red]Error during validation: {str(e)}[/red]")
            session_data['test_result'] = 'failed'
            return session_data

        # Update session data with test results
        all_passed = all(is_valid for _, is_valid in validation_results)
        session_data['test_result'] = 'passed' if all_passed else 'failed'
        session_data['validation_results'] = validation_results
        session_data['files_fixed'] = files_fixed

        # Print summary
        if all_passed:
            console.print("[bold green]✓ All files passed validation![/bold green]")
        else:
            console.print("[bold yellow]⚠ Some files had issues:[/bold yellow]")
            for file_path, is_valid in validation_results:
                status = "✓" if is_valid else "✗"
                color = "green" if is_valid else "red"
                console.print(f"[{color}]{status} {file_path}[/{color}]")

        return session_data

# Initialize Gemini client
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

def fetch_docs(docs_url):
    """Generic method to fetch documentation from a URL."""
    try:
        response = requests.get(docs_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        console.print(f"[red]Error fetching documentation: {str(e)}[/red]")
        return None

# Main CLI
@click.command()
@click.option('--session_name', prompt='Session name', help='Name for your project/session')
def main(session_name):
    ensure_session_dir()
    session_data = load_session(session_name)
    session_data['name'] = session_name

    # Instantiate agents
    agents = [
        QueryAnalyzer(),
        ProjectScaffolder(),
        FeatureImplementer(),
        CodeExplainer(),
        TestAgent(),
    ]

    console.print(f"[bold green]Welcome to the Multi-Agent LLM CLI![/bold green]")
    if not session_data.get('goal'):
        user_goal = Prompt.ask("What would you like to build?")
        session_data['goal'] = user_goal
        save_session(session_name, session_data)
    else:
        user_goal = session_data['goal']
        console.print(f"[cyan]Loaded session:[/cyan] {user_goal}")

    # Main conversational loop
    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]", default=user_goal)
        if user_input.lower() in ["exit", "quit"]:
            console.print("[yellow]Goodbye![/yellow]")
            break
        # Orchestrate agents
        for agent in agents:
            session_data = agent.act({}, user_input, session_data)
        # Save session after each turn
        save_session(session_name, session_data)

if __name__ == "__main__":
    main() 