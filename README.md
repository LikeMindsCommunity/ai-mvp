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
pip install document-parser
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