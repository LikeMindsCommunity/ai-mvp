import os
from typing import List, Optional, Tuple
from google import genai
from google.genai import types
from dotenv import load_dotenv

class CodeGenerationService:
    def __init__(self):
        load_dotenv()
        self.model = "gemini-2.5-pro-exp-03-25"
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.system_instructions = self._load_system_instructions()
        self.generate_content_config = self._setup_config()

    def _load_system_instructions(self) -> List[types.Part]:
        """Load system instructions from files"""
        try:
            with open('./prompt.txt', 'r', encoding='utf-8') as prompt_file:
                prompt_content = prompt_file.read()
            
            with open('./docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            with open('./code.txt', 'r', encoding='utf-8') as code_file:
                code_content = code_file.read()
            
            return [
                types.Part.from_text(text="""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text=f"<flutter-docs>\n\nThis is the entire documentation for context:\n{docs_content}</flutter-docs>"),
                types.Part.from_text(text=f"<flutter-sdk-code>\n\nThis is the code of the entire SDK repository for context:\n{code_content}</flutter-sdk-code>"),
            ]
        except FileNotFoundError as e:
            print(f"Error loading system instructions: {str(e)}")
            return []

    def _setup_config(self):
        """Setup the generation config"""
        return types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=self.system_instructions,
        )

    async def generate_code(self, prompt: str) -> Tuple[bool, Optional[str], Optional[List[str]]]:
        """Generate code based on user prompt"""
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        
        try:
            response_text = ""
            async for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            ):
                chunk_text = chunk.text if not chunk.function_calls else chunk.function_calls[0]
                response_text += chunk_text
            
            # Extract Dart code from the response
            dart_code = self._extract_dart_code(response_text)
            if dart_code:
                return True, dart_code, None
            return False, None, ["No valid Dart code found in the response"]
            
        except Exception as e:
            return False, None, [f"Error generating code: {str(e)}"]

    def _extract_dart_code(self, text: str) -> Optional[str]:
        """Extract Dart code from the response text"""
        import re
        pattern = r"```(?:dart|flutter)?\n(.*?)```"
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            code = match.group(1).strip()
            if any(keyword in code for keyword in ['void main()', 'class', 'import', 'Widget']):
                return code
        return None 