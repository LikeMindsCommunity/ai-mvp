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

1. Install the package:
```bash
pip install document_parser
```

2. Set up your environment variables in a `.env` file as described above.

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

1. Install the package:
```bash
pip install code_generator
```

2. Set up your environment variables in a `.env` file as described above.

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