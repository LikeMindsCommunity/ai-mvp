"""
Generates Flutter code using the Gemini model based on documentation.

Response Types:
- Text: Status updates and progress messages
- Code: Generated code content
- Error: Error messages
"""

import os
from typing import Dict, Optional, Callable, Awaitable, Any, List

from google import genai
from google.genai import types

from flutter_generator.config import Settings

class FlutterCodeGenerator:
    """Generates Flutter code using the Gemini model based on documentation."""

    def __init__(self, settings: Settings = None):
        """
        Initialize the code generator with settings.
        
        Args:
            settings (Settings, optional): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.system_instructions = self._load_system_instructions()
        
        # Configure Google Generative AI client
        self.client = genai.Client(
            api_key=self.settings.google_api_key,
        )
        
        # Setup model and configuration
        self.model = self.settings.gemini_model
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=self.system_instructions,
        )
    
    def _load_system_instructions(self) -> List[types.Part]:
        """
        Load system instructions from files.
        
        Returns:
            List[types.Part]: List of system instruction parts
        """
        try:
            with open('prompt.txt', 'r', encoding='utf-8') as prompt_file:
                prompt_content = prompt_file.read()
            
            with open('docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            with open('code.txt', 'r', encoding='utf-8') as code_file:
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
            print(f"Error loading system instructions: {str(e)}")
            return []
    
    async def generate_code(self, user_prompt: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        """
        Generate code using the Gemini model.
        
        Args:
            user_prompt (str): User input prompt for code generation
            on_chunk (Callable): Callback function for streaming chunks
            
        Returns:
            str: Generated code response
        """
        try:
            # Create content from user prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)],
                ),
            ]
            
            # Generate content with streaming
            response_text = ""
            
            # Get the streaming response
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            )
            
            # Process the stream with a regular for loop
            for chunk in stream:
                # Safely extract text from chunk
                chunk_text = ""
                if hasattr(chunk, 'text') and chunk.text is not None:
                    chunk_text = chunk.text
                elif hasattr(chunk, 'function_calls') and chunk.function_calls:
                    chunk_text = str(chunk.function_calls[0])
                
                # Skip empty chunks
                if not chunk_text:
                    continue
                
                # Stream chunk to client
                await on_chunk({
                    "type": "Code",
                    "value": chunk_text
                })
                
                response_text += chunk_text
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error generating code: {str(e)}"
            await on_chunk({
                "type": "Error",
                "value": error_msg
            })
            return ""
    async def understand_user_query(self, user_query: str) -> Dict[str, Any]:
        """
        Understand the user query by sending it along with the ingested document to the LLM.

        Args:
            user_query (str): The user's input query

        Returns:
            Dict[str, Any]: Response from the LLM based on the user query and ingested document
        """
        try:
            print(f"User Query: {user_query}")
            # Get the absolute path of the ingested document
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ingested_file_path = os.path.join(script_dir, "../../../outputs/test_flutter/document_ingest/ingested/injest.md")

            # Check if the ingested file exists
            if not os.path.exists(ingested_file_path):
                return {"success": False, "error": f"Ingested file not found at {ingested_file_path}"}

            # Read the ingested document
            with open(ingested_file_path, "r", encoding="utf-8") as file:
                ingested_content = file.read()

            # Prepare the prompt for the LLM
            prompt = f"""
            The following is an ingested document for context:
            {ingested_content}

            User Query:
            {user_query}
            """

            # Send the prompt to the LLM
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]

            # Use the updated client configuration
            client_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=self.get_query_understanding_prompt(),
            )

            # Generate content with the LLM
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=client_config,  # Use the updated configuration
            )

            # Extract the response text
            response_text = response.text if hasattr(response, 'text') else ""
            print(f"LLM Response: {response_text}")
            return {"success": True, "response": response_text}

        except Exception as e:
            # Log the exception details
            print(f"Error in understand_user_query: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_query_understanding_prompt() -> str:
        return """# ROLE: Flutter Code Integration Analyst & Query Deconstructor

        ## PRIMARY GOAL:
        Analyze a flattened Flutter project's `lib/` directory codebase and a user query. Deconstruct the query into actionable categories and pinpoint the precise locations (files and specific code areas) where modifications are needed to integrate `likeminds_chat_flutter_core` functionalities.

        ## CONTEXT:
        1.  **Input Code:** You will receive the entire codebase of the `lib/` directory from a Flutter project, flattened into a single text input. Files are delimited (e.g., `--- # filename.dart ---`).
        2.  **User Query:** You will receive a user query describing a desired feature, modification, or bug fix related to integrating chat features.
        3.  **Target SDK:** The integration target is the `likeminds_chat_flutter_core` package. Assume this package is available. Your analysis should identify how to leverage its components.
        4.  **Output Purpose:** Your output will be used by another LLM agent to generate the specific code changes. Therefore, precision in identifying locations and describing the required changes is crucial.

        ## INSTRUCTIONS:

        1.  **Code Comprehension:** Thoroughly read and understand the structure, components (widgets, classes, methods), and overall architecture of the provided flattened `lib/` code.
        2.  **Query Analysis & Categorization:**
            *   Carefully analyze the user query to understand the user's intent.
            *   Categorize the user's requirements into two distinct categories:
                *   **Category 1 (User Code Intent):** What specific changes, features, or functionalities does the user want implemented *directly within their existing Flutter codebase*? (e.g., "Add a button to HomePage", "Navigate to a chat screen from ProfilePage", "Display unread count badge on an existing icon"). This describes the desired *state* of the user's code after integration.
                *   **Category 2 (Agent/Tool Expectation):** What tasks, capabilities, or specific SDK features does the user expect the *agentic tool (or the SDK via the agent)* to provide or handle as part of the solution? (e.g., "Use the pre-built chat list screen", "Handle user authentication/initialization for the chat SDK", "Generate the logic for fetching chatrooms"). This identifies dependencies on the SDK's capabilities or the agent's generation abilities.
        3.  **Identify Modification Targets:**
            *   Based on the code structure and Category 1 (User Code Intent), identify the specific files within the `lib/` directory that require modification.
            *   For each identified file, pinpoint the *exact area* where the change is needed. Be specific:
                *   Name the Widget (e.g., `HomePage`, `ProfilePage`).
                *   Name the Method (e.g., `build`, `onPressed`, `initState`).
                *   Indicate if a new method/widget needs to be added within a class.
                *   Indicate if a new file/class needs to be created.
        4.  **Describe Required Changes (Conceptual):**
            *   For each identified modification target (File + Area), describe *conceptually* what change needs to happen to fulfill the user's intent (Category 1).
            *   Crucially, mention *which components* (classes, methods, widgets) from `likeminds_chat_flutter_core` should be used at that location. (e.g., "In `HomePage`'s `build` method, add an `ElevatedButton`. Its `onPressed` should call `LMChatCore.instance.showChatWithApiKey` and then navigate to `LMChatHomeScreen`.").
            *   This description should be detailed enough to guide a code-generating LLM.

        ## OUTPUT FORMAT (Use Markdown):

        ```markdown
        ## Integration Analysis Report

        **1. User Query Deconstruction:**

        *   **Category 1 (User Code Intent):**
            *   [List the specific features/changes the user wants implemented directly *in their code*. Be concise and action-oriented. Use bullet points.]
            *   Example: Add a 'Chat' button to the `HomePage` Scaffold body.
            *   Example: Implement navigation from the new 'Chat' button to a chat screen.

        *   **Category 2 (Agent/Tool Expectation):**
            *   [List what the user expects the agent/tool or the SDK to handle or provide. Use bullet points.]
            *   Example: Utilize the `likeminds_chat_flutter_core`'s standard chat home screen (`LMChatHomeScreen`).
            *   Example: Handle the necessary SDK initialization (`LMChatCore.instance.showChatWithApiKey`) using provided credentials.

        **2. Code Modification Plan:**

        *   **File:** `lib/path/to/file1.dart`
            *   **Area:** `WidgetName` > `methodName` (e.g., `HomePage` > `build`)
                *   **Required Change:** [Describe the conceptual change needed here, referencing Category 1 goals and specifying `likeminds_chat_flutter_core` components. E.g., "Add an `ElevatedButton` widget within the `Column`. Text should be 'Go to Chat'."]
            *   **Area:** `WidgetName` > `onPressed` callback for the new Button (or existing button)
                *   **Required Change:** [E.g., "Implement asynchronous call to `LMChatCore.instance.showChatWithApiKey` using hardcoded user UUID 'test_user_123' and userName 'Test User'. Check the response success. If successful, use `Navigator.push` with `MaterialPageRoute` to navigate to `LMChatHomeScreen`."]
            *   **Area:** Top of file / Class level (if needed)
                *   **Required Change:** [E.g., "Add import for `package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart`."]

        *   **File:** `lib/path/to/another_file.dart` (If changes are needed in multiple files)
            *   **Area:** ...
                *   **Required Change:** ...

        *   **New File (If applicable):** `lib/features/chat/new_screen.dart`
            *   **Purpose:** [Describe why this new file/screen is needed, based on Category 1/2.]
            *   **Required Change:** [Describe the basic structure and the core `likeminds_chat_flutter_core` component to be used, e.g., "Create a `StatelessWidget` that returns `LMChatHomeScreen` in its build method."]

        **3. Data/Configuration Notes:**
        *   [Mention any specific data needed (like API Keys, User IDs) and where the query indicates they should come from (or if they are missing/need to be assumed/hardcoded).]
        *   [Note any assumptions made about SDK setup or available data.]
        """