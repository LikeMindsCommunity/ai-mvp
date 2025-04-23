# LikeMinds Flutter Integration Assistant

An AI-powered API service that generates and tests Flutter code integrations for LikeMinds Chat and Feed SDKs.

## Overview

This project uses the Gemini 2.5 Pro API to generate Flutter integration code based on user prompts. It helps developers quickly implement LikeMinds SDK features by providing complete, ready-to-run code samples through a WebSocket API.

## Features

- WebSocket API for generating Flutter integration code
- Real-time streaming of generation output
- Automatic code analysis and error detection
- Code deployment to a test Flutter project for immediate verification
- Web build and hosting for easy viewing of the generated app
- Interactive error handling and code regeneration

## Prerequisites

- Python 3.7+
- Flutter SDK installed and configured
- Google Gemini API key

## Structure

   project/
   ├── api/
   │   ├── domain/interfaces/
   │   ├── infrastructure/services/
   │   └── presentation/
   ├── flutter_generator/
   │   ├── config/
   │   ├── core/
   │   └── utils/
   ├── integration/
   ├── output/
   │   └── {project_id}/
   │       ├── integration/
   │       └── generations/
   │           └── {generation_id}.dart
   └── run_server.py

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Start the API server:

```
python run_server.py
```

The WebSocket endpoint will be available at `ws://localhost:8000/api/flutter`.

### API Format

To generate Flutter code, send a WebSocket message in this format:

```json
{
  "type": "GenerateCode",
  "user_query": "Create a Flutter chat screen using LikeMinds SDK",
  "session_id": "optional-session-identifier"
}
```

To generate only a conversational explanation and plan:

```json
{
  "type": "GenerateConversation",
  "user_query": "Create a Flutter chat screen using LikeMinds SDK",
  "session_id": "optional-session-identifier"
}
```

To fix code with errors:

```json
{
  "type": "FixCode",
  "user_query": "Original query text",
  "error_message": "Flutter analysis error message",
  "session_id": "optional-session-identifier"
}
```

The `session_id` is optional but recommended to maintain conversation history across requests.

### Authentication APIs

The service provides the following authentication endpoints:

#### User Registration and Authentication
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "User Name"
}

POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

POST /api/auth/logout
Authorization: Bearer <access_token>
```

#### OAuth Authentication (GitHub)
```http
POST /api/auth/github
# Returns GitHub OAuth URL for sign-in

GET /api/auth/github/callback?session=<session>
# GitHub OAuth callback endpoint
```

#### User Profile Management
```http
GET /api/users/me
Authorization: Bearer <access_token>

PUT /api/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Updated Name",
  "avatar_url": "https://..."
}
```

#### Project Management
```http
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Project Name",
  "description": "Project Description"
}

GET /api/projects/
Authorization: Bearer <access_token>

GET /api/projects/{project_id}
Authorization: Bearer <access_token>

PUT /api/projects/{project_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated Description"
}

DELETE /api/projects/{project_id}
Authorization: Bearer <access_token>

POST /api/projects/{project_id}/share
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_email": "collaborator@example.com",
  "role": "viewer"
}
```

### Environment Variables

In addition to the Google API key, you'll need these environment variables for authentication:

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Frontend Configuration
FRONTEND_URL=http://localhost:8080
FRONTEND_CALLBACK_PATH=/auth/callback
```


### Response Format

The API will stream responses in this format:

```json
{
  "type": "Text|Code|Chat|Error|Success|AnalysisError|Result",
  "value": "Message content or object"
}
```

Response types are used as follows:
- `Text`: Status updates and progress messages
- `Code`: Generated code content
- `Chat`: Conversational explanations and generation plans
- `Error`: Error messages
- `Success`: Success notifications
- `AnalysisError`: Flutter code analysis errors
- `Result`: Final result with URL and file path information

## Project Structure

The project follows a clean architecture pattern with these main components:

- `api/` - WebSocket API with clean architecture layers
  - `presentation/` - WebSocket handlers
  - `domain/` - Business logic interfaces
  - `infrastructure/` - Service implementations
- `flutter_generator/` - Core Flutter code generation
  - `core/` - Core generator functionality
  - `config/` - Configuration settings
  - `utils/` - Utility functions
- `integration/` - Template Flutter project used as a base for code deployment
- `output/` - Directory for projects and generated code
  - `{project_id}/` - One directory per project
    - `integration/` - Flutter test project specific to this project
    - `generations/` - All code generations for this project

## Code Generation Flow

The service follows an efficient project-based generation model:

1. Each project gets its own directory and Flutter integration environment
2. Multiple generations within the same project reuse the same Flutter environment
3. Each generation is stored as a separate file but deployed to the same integration environment
4. This approach optimizes resource usage while maintaining isolation between different projects

## License

Copyright LikeMinds, Inc. 