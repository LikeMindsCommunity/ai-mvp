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
HAWCX_DOCS_URL = "https://docs.hawcx.com/llms-full.txt"

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

        # Get Hawcx docs and API key if authentication is needed
        hawcx_docs = None
        hawcx_api_key = None
        if needs_auth:
            hawcx_api_key = session_data.get('hawcx_api_key') or Prompt.ask("Enter your Hawcx API Key")
            session_data['hawcx_api_key'] = hawcx_api_key
            hawcx_docs = session_data.get('hawcx_docs')
            if not hawcx_docs:
                hawcx_docs = fetch_hawcx_docs()
                session_data['hawcx_docs'] = hawcx_docs

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
            prompt = f"""Generate a complete JavaScript web application that includes both the requested features and Hawcx passwordless authentication. Return a JSON array of files as specified in the requirements.

Requirements: {requirements}

Hawcx docs:
{hawcx_docs}

API Key: {hawcx_api_key}

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
                console.print(f"[green]Features implemented with Hawcx authentication[/green]")
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

        # Read all project files
        files_content = {}
        for file in ['main.js', 'index.html', 'package.json']:
            file_path = os.path.join(project_dir, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    files_content[file] = f.read()

        # Generate README content using LLM
        client = get_gemini_client()
        prompt = f"""Generate a comprehensive README.md for a JavaScript project with Hawcx authentication. Include:
1. Project overview
2. Features
3. Setup instructions
4. How to run the project
5. Code structure explanation
6. Authentication flow explanation

Project files content:
{json.dumps(files_content, indent=2)}

Return only the README.md content in markdown format without any additional text or explanations."""
        
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        readme_content = response.text

        # Write README.md
        readme_path = os.path.join(project_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)

        console.print(f"[green]README.md generated with project documentation[/green]")
        return session_data

# Test Agent
class TestAgent(Agent):
    def __init__(self):
        super().__init__("TestAgent", "Generates and runs tests, fixes errors.")

    def act(self, context, user_input, session_data):
        project_dir = session_data.get('project_dir')
        if not project_dir:
            return session_data

        # Test 1: Check if required files exist
        required_files = ['main.js', 'index.html', 'package.json']
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(project_dir, f))]
        if missing_files:
            console.print(f"[red]Missing required files: {', '.join(missing_files)}[/red]")
            session_data['test_result'] = 'failed'
            return session_data

        # Test 2: Validate JavaScript syntax
        try:
            result = subprocess.run(["node", "--check", "main.js"], cwd=project_dir, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                console.print(f"[red]JavaScript syntax error in main.js:[/red]\n{result.stderr}")
                session_data['test_result'] = 'failed'
                # Attempt to fix syntax errors
                client = get_gemini_client()
                with open(os.path.join(project_dir, "main.js"), "r") as f:
                    code = f.read()
                prompt = f"The following JavaScript code has syntax errors. Please fix them and return only the corrected code without any explanations:\n\n{code}"
                response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
                fixed_code = response.text
                with open(os.path.join(project_dir, "main.js"), "w") as f:
                    f.write(fixed_code)
                console.print(f"[yellow]Fixed syntax errors in main.js. Re-running tests...[/yellow]")
                return self.act(context, user_input, session_data)
            else:
                console.print(f"[green]JavaScript syntax validation passed![/green]")
                session_data['test_result'] = 'passed'
        except Exception as e:
            console.print(f"[red]Error checking JavaScript syntax: {e}[/red]")
            session_data['test_result'] = 'failed'

        return session_data

# Initialize Gemini client
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

def fetch_hawcx_docs():
    response = requests.get(HAWCX_DOCS_URL)
    response.raise_for_status()
    return response.text

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