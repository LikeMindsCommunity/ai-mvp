# LikeMinds Android Feed SDK Code Generator

This project provides tools for generating code for the LikeMinds Android Feed SDK using AI.

## Features

- Documentation parsing and processing
- AI-powered code generation using Gemini 2.5 Pro
- Interactive code generation interface
- Streaming and non-streaming output options

## Project Structure

```
ai-mvp/
├── code_generator/           # Main code generation package
│   ├── core/                # Core functionality
│   │   └── generator.py     # Code generation logic
│   ├── config/              # Configuration
│   │   └── settings.py      # Settings and defaults
│   ├── utils/               # Utilities
│   │   └── documentation.py # Documentation handling
│   ├── __init__.py          # Package initialization
│   └── __main__.py          # Main entry point
├── document_parser.py        # Documentation parsing utility
├── combined_documentation.md # SDK documentation
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Gemini API key and model name:
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL_NAME=gemini-2.5-pro-exp-03-25
   ```

## Usage

### Documentation Parser

To parse and process the SDK documentation:
```bash
python document_parser.py
```

### Code Generator

To start the interactive code generator:
```bash
python -m code_generator
```

The code generator will:
1. Load the SDK documentation
2. Provide an interactive interface
3. Generate code based on your requests
4. Support both streaming and non-streaming output

## Default Values

The code generator uses the following default values:
- API Key: `701a4436-6bab-45b7-92e5-a1c61763e229`
- Model Name: `gemini-2.5-pro-exp-03-25`
- Username: `test`

These values are automatically used when generating code that requires authentication.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
