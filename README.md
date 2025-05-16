# Multi-Agent LLM CLI

This CLI tool uses Google Gemini LLM and a multi-agent system to scaffold plain JavaScript projects, integrate Hawcx passwordless authentication, and provide explanations and automated testing.

## Features
- Conversational, multi-agent LLM-powered CLI
- Scaffolds vanilla JS projects
- Integrates Hawcx passwordless authentication (prompts for your API key)
- Explains code and integration steps
- Generates and runs tests, fixes errors automatically
- Remembers your session/project state

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the CLI:

```bash
python multiagent_cli.py
```

3. Follow the prompts to describe your project and provide your Hawcx API key.

## Requirements
- Python 3.8+
- Node.js (for running JS code/tests)

## Notes
- Your Gemini API key is pre-configured.
- Your Hawcx API key will be requested during setup.
- All project files and session data are stored locally.
