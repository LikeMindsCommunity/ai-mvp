import base64
import glob
import os
import re
import time
import signal
import subprocess
import argparse
import threading
from typing import List, Tuple, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import print as rprint
from rich.syntax import Syntax
from rich.live import Live
from rich.table import Table
from rich.prompt import Prompt

# Initialize rich console
console = Console()

# Initialize Gemini client
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# Define a timeout handler for commands
class CommandTimeoutError(Exception):
    """Exception raised when a command times out."""
    pass

def run_command_with_timeout(cmd, timeout=30):
    """Run a command with timeout and return (exit_code, output)"""
    process = subprocess.Popen(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True
    )
    
    output = []
    def collect_output():
        for line in process.stdout:
            output.append(line)
    
    thread = threading.Thread(target=collect_output)
    thread.daemon = True
    thread.start()
    
    try:
        exit_code = process.wait(timeout=timeout)
        thread.join(timeout=1)
        return exit_code, ''.join(output)
    except subprocess.TimeoutExpired:
        process.kill()
        return -1, "Command timed out after {} seconds".format(timeout)

class FlutterCodeGenerator:
    def __init__(self):
        self.model = "gemini-2.5-pro-exp-03-25"
        self.system_instructions = self._load_system_instructions()
        self.generate_content_config = None
        self.setup_config()
    
    def _load_system_instructions(self) -> List[types.Part]:
        """Load system instructions from files"""
        try:
            with open('api/prompt.txt', 'r', encoding='utf-8') as prompt_file:
                prompt_content = prompt_file.read()
            
            with open('api/docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            with open('api/code.txt', 'r', encoding='utf-8') as code_file:
                code_content = code_file.read()
            
            return [
                types.Part.from_text(text="""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text="""<flutter-docs>
                \n\nThis is the entire documentation for context:
                """ + docs_content + """</flutter-docs>"""),
                types.Part.from_text(text="""<flutter-sdk-code>
                \n\nThis is the code of the entire SDK repository for context:
                """ + code_content + """</flutter-sdk-code>"""),
            ]
        except FileNotFoundError as e:
            console.print(f"[bold red]Error loading system instructions: {str(e)}[/bold red]")
            return []
    
    def setup_config(self):
        """Setup the generation config"""
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=self.system_instructions,
        )
    
    def generate_code(self, user_prompt: str, progress: Progress = None) -> str:
        """Generate code based on user prompt"""
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_prompt)],
            ),
        ]
        
        try:
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            ):
                chunk_text = chunk.text if not chunk.function_calls else chunk.function_calls[0]
                console.print(chunk_text, end='', style="bright_white")
                response_text += chunk_text
            return response_text
        except Exception as e:
            console.print(f"[bold red]Error generating code: {str(e)}[/bold red]")
            return ""

class FlutterCodeManager:
    def __init__(self):
        self.latest_code = None
        self.integration_path = "integration"
        self.root_dir = os.getcwd()  # Store the root directory
    
    def extract_dart_code(self, text: str) -> List[str]:
        """Extract Dart code blocks from text"""
        pattern = r"```(?:dart|flutter)?\n(.*?)```"
        matches = re.finditer(pattern, text, re.DOTALL)
        dart_codes = []
        
        for match in matches:
            code = match.group(1).strip()
            if any(keyword in code for keyword in ['void main()', 'class', 'import', 'Widget']):
                dart_codes.append(code)
        
        return dart_codes
    
    def save_dart_code(self, code: str, index: int = 0) -> str:
        """Save Dart code to file and return the filename"""
        # Make sure we're in the root directory
        os.chdir(self.root_dir)
        
        os.makedirs('output', exist_ok=True)
        filename = f'output/flutter_code_{index + 1}.dart'
        
        with open(filename, 'w') as f:
            f.write(code)
        
        dart_syntax = Syntax(code, "dart", theme="monokai", line_numbers=True)
        console.print(Panel(
            dart_syntax,
            title=f"[bold green]Generated Dart Code - Saved to {filename}[/bold green]",
            border_style="green"
        ))
        
        self.latest_code = code
        return filename
    
    def analyze_flutter_code(self) -> Tuple[bool, str]:
        """Analyze Flutter code for errors"""
        console.print("[yellow]Analyzing Flutter code (max 15 seconds)...[/yellow]")
        
        exit_code, output = run_command_with_timeout(
            'flutter analyze lib/main.dart --no-fatal-infos', 
            timeout=15
        )
        
        if exit_code != 0:
            return False, output
        return True, ""
    
    def copy_to_integration(self, source_file: str) -> bool:
        """Copy generated code to integration project"""
        try:
            # Make sure we're in the root directory
            os.chdir(self.root_dir)
            
            with open(source_file, 'r') as source:
                code = source.read()
            
            # Ensure integration directory exists with lib subfolder
            os.makedirs(os.path.join(self.integration_path, 'lib'), exist_ok=True)
            
            main_dart_path = os.path.join(self.integration_path, 'lib/main.dart')
            with open(main_dart_path, 'w') as target:
                target.write(code)
            
            return True
        except Exception as e:
            console.print(f"[bold red]Error copying code: {str(e)}[/bold red]")
            return False

class FlutterIntegrationManager:
    def __init__(self):
        self.code_generator = FlutterCodeGenerator()
        self.code_manager = FlutterCodeManager()
    
    def run_integration_flow(self, user_prompt: Optional[str] = None) -> bool:
        """Run the complete integration flow with better conversation flow"""
        if not user_prompt:
            user_prompt = console.input("[cyan]Enter your Flutter integration question: [/cyan]")
        
        console.print("[bold blue]Generating Flutter code based on your request...[/bold blue]")
        
        # Generate code
        response = self.code_generator.generate_code(user_prompt)
        if not response:
            console.print("[bold red]Failed to generate code. Please try again.[/bold red]")
            return False
            
        # Extract and save code
        console.print("[cyan]Processing generated code...[/cyan]")
        dart_codes = self.code_manager.extract_dart_code(response)
        if not dart_codes:
            console.print("[bold red]No valid Dart code found in the response[/bold red]")
            return False
        
        latest_file = self.code_manager.save_dart_code(dart_codes[0])
        
        # Copy to integration project
        console.print("[cyan]Setting up integration...[/cyan]")
        if not self.code_manager.copy_to_integration(latest_file):
            return False
        
        # Change to integration directory
        os.chdir(self.code_manager.integration_path)
        
        # Run Flutter commands
        console.print("[yellow]Running flutter pub get...[/yellow]")
        exit_code, output = run_command_with_timeout('flutter pub get', timeout=30)
        if exit_code != 0:
            console.print(f"[bold red]Error running flutter pub get:[/bold red]\n{output}")
            # Return to root directory
            os.chdir(self.code_manager.root_dir)
            return False
        
        # Analyze code
        success, error_message = self.code_manager.analyze_flutter_code()
        
        if not success:
            console.print(Panel(
                "[bold red]Flutter code analysis found errors:[/bold red]\n" +
                f"[white]{error_message}[/white]",
                border_style="red"
            ))
            
            # Use simple yes/no without using Rich prompt which can cause issues
            console.print("[yellow]Would you like to regenerate with fixes? (y/n)[/yellow]")
            response = input().strip().lower()
            
            if response == 'y':
                # Return to root directory before regenerating
                os.chdir(self.code_manager.root_dir)
                console.print("[bold yellow]Regenerating with error fixes...[/bold yellow]")
                enhanced_prompt = f"{user_prompt}\n\nPlease fix these errors:\n{error_message}"
                return self.run_integration_flow(enhanced_prompt)
            
            # Return to root directory before exiting
            os.chdir(self.code_manager.root_dir)
            return False
        
        # Run the app
        console.print("[yellow]Running flutter run...[/yellow]")
        exit_code, output = run_command_with_timeout('flutter run', timeout=6000)
        if exit_code != 0:
            console.print(f"[bold red]Error running flutter run:[/bold red]\n{output}")
            # Return to root directory
            os.chdir(self.code_manager.root_dir)
            return False
            
        console.print(Panel("[bold green]✨ Integration completed successfully! ✨[/bold green]",
                          border_style="green"))
        
        # Return to root directory before exiting
        os.chdir(self.code_manager.root_dir)
        return True

def main():
    parser = argparse.ArgumentParser(description='LikeMinds Flutter Integration Assistant')
    parser.add_argument('--prompt', type=str, help='Initial integration prompt', default=None)
    args = parser.parse_args()
    
    console.print(Panel(
        "[bold blue]LikeMinds Flutter Integration Assistant[/bold blue]\n" +
        "[cyan]Starting the integration process...[/cyan]",
        border_style="blue"
    ))
    
    integration_manager = FlutterIntegrationManager()
    integration_manager.run_integration_flow(args.prompt)

if __name__ == "__main__":
    main()
