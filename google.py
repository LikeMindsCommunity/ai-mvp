import base64
import glob
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def extract_dart_code(text):
    # Pattern to match code blocks with dart, flutter, or no language specified
    pattern = r"```(?:dart|flutter)?\n(.*?)```"
    matches = re.finditer(pattern, text, re.DOTALL)
    dart_codes = []
    
    for match in matches:
        code = match.group(1).strip()
        # Basic validation to check if it's Dart code
        if any(keyword in code for keyword in ['void main()', 'class', 'import', 'Widget']):
            dart_codes.append(code)
    
    return dart_codes

def save_dart_code(code, index=0):
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Determine the filename
    filename = f'output/flutter_code_{index + 1}.dart'
    
    with open(filename, 'w') as f:
        f.write(code)
    print(f"\nSaved Dart code to: {filename}")

def get_md_files_content(directory):
    combined_content = []
    # Get all .md files in current directory
    md_files = glob.glob(os.path.join(directory, '*.md'))
    
    # Process files in current directory
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                relative_path = os.path.relpath(file_path, directory)
                content = file.read()
                combined_content.append(f"File: {relative_path}\n\n{content}\n\n---\n\n")
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
    
    # Look for subdirectories
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # Recursively get content from subdirectories
            combined_content.extend(get_md_files_content(item_path))
    
    return combined_content

def generate():
    prompt_content=""
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    with open('prompt.txt', 'r') as file:
        prompt_content = file.read()
    
    docs_path = 'docs/chat'
    markdown_contents = get_md_files_content(docs_path)
    
    # Join all content into a single string
    all_docs_content = "".join(markdown_contents)

    model = "gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""How do I integrate LikeMinds Chat SDK in Flutter?"""),
                types.Part.from_text(text="How do I customise the appbar of the chatroom screen?"),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps."""),
            types.Part.from_text(text=prompt_content),
            types.Part.from_text(text=all_docs_content),
        ],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        chunk_text = chunk.text if not chunk.function_calls else chunk.function_calls[0]
        print(chunk_text, end='')
        response_text += chunk_text
    
    # Extract and save any Dart code found in the response
    dart_codes = extract_dart_code(response_text)
    if dart_codes:
        print("\n\nFound Flutter/Dart code in the response. Saving to files...")
        for i, code in enumerate(dart_codes):
            save_dart_code(code, i)

if __name__ == "__main__":
    generate()
