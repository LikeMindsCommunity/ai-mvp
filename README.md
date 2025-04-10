# Document Parser

A Python package for processing and combining markdown documentation from Git repositories.

## Environment Variables

The package requires the following environment variables to be set in your `.env` file:

- `REPO_URL` (Required): The URL of the Git repository containing the markdown documentation.
- `INCLUDED_DIRS` (Required): Comma-separated list of directories to include in the documentation processing.
- `EXCLUDED_DIRS` (Optional): Comma-separated list of directories to exclude from the documentation processing.
- `OUTPUT_FILE` (Required): The path where the combined documentation will be saved.

Example `.env` file:
```
# Document Parser Configuration
REPO_URL=https://github.com/LikeMindsCommunity/likeminds-docs
INCLUDED_DIRS=feed/Android
EXCLUDED_DIRS=feed/Android/Data
OUTPUT_FILE=document_parser/single_file/feed_android_documentation.md
```

## Package Usage

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Use the package in your Python code:
```python
from document_parser.core import DocumentParser
from document_parser.config import Settings

# Initialize settings and parser
settings = Settings()
parser = DocumentParser(settings)

# Generate combined documentation
parser.generate_combined_document()
```

Or run it directly from the command line:
```bash
python -m document_parser
```

## Functionality

The Document Parser package provides the following features:

1. **Repository Cloning**: Automatically clones the specified Git repository.
2. **Selective Processing**: Processes only the specified directories while excluding others.
3. **Markdown Processing**:
   - Extracts and organizes headings
   - Converts relative links to proper references
   - Handles GitHub links and fetches their content
4. **Documentation Generation**:
   - Creates a combined markdown document
   - Preserves the original structure with proper heading levels
   - Includes a summary of subheadings for each file
   - Appends GitHub file contents at the end of the document
5. **Cleanup**: Automatically removes the cloned repository after processing

The generated documentation will include:
- File paths as main headings
- Subheadings summary for each file
- Processed content with proper heading levels
- GitHub file contents (if referenced)
- Properly formatted links and references

## Error Handling

The package includes comprehensive error handling for:
- Repository cloning failures
- File processing errors
- GitHub content fetching issues
- Environment variable validation
- File system operations

All errors are logged with descriptive messages to help with debugging.

# Code Generator

A Python package for generating Android projects using the Gemini model based on documentation.

## Environment Variables

The package requires the following environment variables to be set in your `.env` file:

- `GEMINI_API_KEY` (Required): The API key for accessing the Gemini model.
- `GEMINI_MODEL_NAME` (Required): The name of the Gemini model to use (currently only supports "gemini-2.5-pro-exp-03-25").
- `TEMPLATE_REPO_URL` (Required): The URL of the template repository containing the base Android project structure.
- `OUTPUT_FILE` (Required): The path to the documentation file that will be used for code generation.
- `OUTPUT_DIR` (Required): The directory where generated projects will be saved.

Example `.env` file:
```
# Code Generator Configuration
GEMINI_API_KEY=AIzaSyAwt6GCUzyXo0TBDSJZ53_KDUH4H3tOfxc
GEMINI_MODEL_NAME=gemini-2.5-pro-exp-03-25
TEMPLATE_REPO_URL=https://github.com/LikeMindsCommunity/likeminds-feed-android-social-feed-theme
OUTPUT_DIR=code_generator/generated_projects
```

## Package Usage

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Use the package in your Python code:
```python
from code_generator.core import CodeGenerator
from code_generator.config import Settings

# Initialize settings and generator
settings = Settings()
generator = CodeGenerator(settings)

# Run the generator in interactive mode
generator.run()
```

Or run it directly from the command line:
```bash
python -m code_generator
```

## Functionality

The Code Generator package provides the following features:

1. **Documentation Processing**: Reads and processes documentation to understand the LikeMinds Feed SDK requirements.
2. **Template Management**: Uses a template repository to maintain consistent project structure.
3. **Code Generation**:
   - Uses Gemini AI model to generate Android project code
   - Creates complete project structure with all necessary files
   - Includes build configuration files (build.gradle, settings.gradle, etc.)
   - Generates proper Kotlin code following Android best practices
4. **Project Creation**:
   - Creates complete Android project directories
   - Copies necessary Gradle wrapper files
   - Generates all required source files
   - Maintains proper project structure
5. **Interactive Mode**: Provides a user-friendly command-line interface for project generation.

The generated projects include:
- Complete Android project structure
- Build configuration files
- Source code files
- Proper package organization
- Default configuration (username and API key)

## Error Handling

The package includes comprehensive error handling for:
- API key validation
- Model name validation
- Template repository access
- Documentation file validation
- Project creation errors
- JSON parsing errors
- File system operations

All errors are logged with descriptive messages to help with debugging.

# API

A FastAPI-based WebSocket API for generating Android projects using the code generator package.

## Deployment

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the API server:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

4. The API will be available at:
- WebSocket endpoint: `ws://localhost:8000/api/ttandroid`
- API documentation: `http://localhost:8000/docs`

## API Endpoints

### WebSocket Endpoint: `/api/ttandroid`

A WebSocket endpoint for real-time code generation and project creation.

#### Request Format
```json
{
    "user_query": "string"  // The query describing the project to generate
}
```

#### Response Format
The API sends multiple responses during the generation process:

1. **Text Updates** (type: "Text")
```json
{
    "type": "Text",
    "value": "string"  // Progress updates or generated code chunks
}
```

2. **Error Messages** (type: "Error")
```json
{
    "type": "Error",
    "value": "string"  // Error message describing what went wrong
}
```

3. **Final Result** (type: "Result")
```json
{
    "type": "Result",
    "value": {
        "success": boolean  // Whether the project was generated successfully
    }
}
```

#### Example Usage

1. Connect to the WebSocket endpoint:
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ttandroid');
```

2. Send a generation request:
```javascript
ws.send(JSON.stringify({
    "user_query": "Create a social feed app with LikeMinds Feed SDK"
}));
```

3. Handle responses:
```javascript
ws.onmessage = (event) => {
    const response = JSON.parse(event.data);
    switch(response.type) {
        case "Text":
            console.log("Progress:", response.value);
            break;
        case "Error":
            console.error("Error:", response.value);
            break;
        case "Result":
            console.log("Generation complete:", response.value);
            break;
    }
};
```

#### Error Handling

The API handles various error cases:
- Invalid request format
- Missing user_query
- Code generation failures
- WebSocket connection issues

All errors are returned with a descriptive message in the Error response format. 