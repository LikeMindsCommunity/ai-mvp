# Document Ingest

A Python package for ingesting and processing documentation and SDK code for the LikeMinds Feed SDK.

## Environment Variables

The package requires the following environment variables to be set in your `.env` file:

- `DOCS_PATH` (Required): The path to the documentation file that will be used for code generation.
- `SDK_CODE_PATH` (Required): The path to the SDK code reference file.

Example `.env` file:
```
# Document Ingest Configuration
DOCS_PATH=document_ingest/ingested/likeminds-docs-feed-android.md
SDK_CODE_PATH=document_ingest/ingested/likeminds-feed-android.md
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
from document_ingest.core import DocumentIngest
from document_ingest.config import Settings

# Initialize settings and ingest
settings = Settings()
ingest = DocumentIngest(settings)

# Process documentation and SDK code
ingest.process()
```

Or run it directly from the command line with the following arguments:
```bash
python -m document_ingest https://github.com/LikeMindsCommunity/likeminds-docs --include feed/Android --exclude feed/Android/Data
```

Command-line Arguments:
- `repo_url` (Required, positional): The URL of the Git repository containing the documentation
- `--private` (Optional, flag): Indicates if the repository is private
- `--include` (Optional): List of directories to include in the documentation processing
- `--exclude` (Optional): List of directories to exclude from the documentation processing
- `--private-repo-name` (Optional): Custom name for the private repository

Example with all arguments:
```bash
python -m document_ingest https://github.com/LikeMindsCommunity/likeminds-docs \
    --private \
    --include feed/Android feed/iOS \
    --exclude feed/Android/Data feed/iOS/Data \
    --private-repo-name likeminds-docs
```

## Functionality

The Document Ingest package provides the following features:

1. **Documentation Processing**: 
   - Reads and processes LikeMinds Feed SDK documentation
   - Extracts relevant information for code generation
   - Maintains proper structure and formatting

2. **SDK Code Processing**:
   - Processes SDK code reference files
   - Extracts method signatures and implementations
   - Maintains proper code structure

3. **Output Generation**:
   - Creates processed documentation files
   - Generates SDK code reference files
   - Ensures proper file organization

## Error Handling

The package includes comprehensive error handling for:
- File path validation
- File content processing
- Output generation
- File system operations

All errors are logged with descriptive messages to help with debugging.

# Code Generator

A Python package for generating Android projects using the Gemini model based on documentation.

## Environment Variables

The package requires the following environment variables to be set in your `.env` file:

- `GEMINI_API_KEY` (Required): The API key for accessing the Gemini model.
- `GEMINI_MODEL_NAME` (Required): The name of the Gemini model to use (currently only supports "gemini-2.5-pro-exp-03-25").
- `TEMPLATE_REPO_URL` (Required): The URL of the template repository containing the base Android project structure.
- `OUTPUT_DIR` (Required): The directory where generated projects will be saved.
- `DOCS_PATH` (Required): The path to the documentation file that will be used for code generation.
- `SDK_CODE_PATH` (Required): The path to the SDK code reference file.

Example `.env` file:
```
# Code Generator Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-pro-exp-03-25
TEMPLATE_REPO_URL=https://github.com/LikeMindsCommunity/likeminds-feed-android-social-feed-theme
OUTPUT_DIR=code_generator/generated_projects
DOCS_PATH=document_ingest/ingested/likeminds-docs-feed-android.md
SDK_CODE_PATH=document_ingest/ingested/likeminds-feed-android.md
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
   - Ensures proper method signatures and return types
   - Handles callback implementations correctly
   - Follows Android best practices
4. **Project Creation**:
   - Creates complete Android projects
   - Sets up proper package structure
   - Configures build files
   - Handles dependencies

## Error Handling

The package includes comprehensive error handling for:
- Environment variable validation
- API key verification
- Model response parsing
- File system operations
- Project generation errors

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