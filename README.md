# LikeMinds Flutter Integration Assistant

An AI-powered API service that generates and tests Flutter code integrations for LikeMinds Chat and Feed SDKs.

## Overview

This project uses the Gemini 2.5 Pro API to generate Flutter integration code based on user prompts. It helps developers quickly implement LikeMinds SDK features by providing complete, ready-to-run code samples through a WebSocket API. The service handles code generation, analysis, deployment, and testing in a unified workflow.

## Features

- WebSocket API for generating Flutter integration code
- Real-time streaming of generation output
- Automatic code analysis and error detection
- Code deployment to a test Flutter project for immediate verification
- Web build and hosting for easy viewing of the generated app
- Interactive error handling and code regeneration
- User authentication and project management
- Docker containerization for easy deployment
- Supabase integration for user and project data storage

## Prerequisites

- Python 3.7+
- Flutter SDK installed and configured
- Google Gemini API key
- Supabase account (for authentication)
- Docker and Docker Compose (optional, for containerized deployment)

## Structure

```
project/
├── api/                          # API implementation
│   ├── domain/interfaces/        # Business logic interfaces
│   ├── infrastructure/services/  # Service implementations
│   └── presentation/             # WebSocket and REST handlers
├── flutter_generator/            # Flutter code generation
│   ├── config/                   # Configuration settings
│   ├── core/                     # Core generator functionality
│   └── utils/                    # Utility functions
├── integration/                  # Template Flutter project
├── output/                       # Generated code output
│   └── {project_id}/
│       ├── integration/          # Project-specific Flutter environment
│       └── generations/          # Individual code generations
│           └── {generation_id}.dart
├── docker/                       # Docker configuration
│   ├── Dockerfile                # Container definition
│   ├── docker-compose.yml        # Multi-container setup
│   └── docker-compose.env.example # Environment variables template
├── docs/                         # Documentation
│   ├── plans/                    # Architecture plans
│   └── implementation/           # Implementation details
├── supabase/                     # Supabase configuration
├── tools/                        # Utility scripts
└── run_server.py                 # Main entry point
```

## Installation

### Local Setup

1. Clone this repository
   ```
   git clone https://github.com/likeminds-inc/flutter-integration-assistant.git
   cd flutter-integration-assistant
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required environment variables you can check in the `env.example` file:
   ```
   # Google Generative AI API
   GOOGLE_API_KEY=your_api_key_here
   
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_KEY=your_supabase_service_key
   
   # Frontend Configuration
   FRONTEND_URL=http://localhost:8080
   FRONTEND_CALLBACK_PATH=/auth/callback
   ```

5. Ensure the required support files exist:
   - `prompt.txt`: LLM prompt template
   - `docs.txt`: SDK documentation
   - `code.txt`: Example SDK code

### Docker Setup

1. Navigate to the Docker directory:
   ```
   cd docker
   ```

2. Copy the example environment file and configure:
   ```
   cp docker-compose.env.example .env
   # Edit .env and add your configuration
   ```

3. Build and start the containers:
   ```
   docker-compose up -d
   ```

4. The service will be available at:
   - WebSocket: `ws://localhost:8000/api/flutter`
   - Health check: `http://localhost:8000/`
   - Web previews: `http://localhost:8080/`

## Usage

### Starting the API Server

Start the API server locally:

```
python run_server.py
```

The WebSocket endpoint will be available at `ws://localhost:8000/api/flutter`.

### WebSocket API Format

#### Generate Flutter Code

```json
{
  "type": "GenerateCode",
  "user_query": "Create a Flutter chat screen using LikeMinds SDK",
  "session_id": "optional-session-identifier"
}
```

#### Update Existing Generation

```json
{
  "type": "GenerateCode",
  "user_query": "Create a Flutter chat screen using LikeMinds SDK",
  "update_existing": true,
  "session_id": "optional-session-identifier"
}
```

#### Generate Conversational Plan Only

```json
{
  "type": "GenerateConversation",
  "user_query": "Create a Flutter chat screen using LikeMinds SDK",
  "session_id": "optional-session-identifier"
}
```

#### Fix Code with Errors

```json
{
  "type": "FixCode",
  "user_query": "Original query text",
  "error_message": "Flutter analysis error message",
  "session_id": "optional-session-identifier"
}
```

#### Fix Code with Errors, Updating Existing Generation

```json
{
  "type": "FixCode",
  "user_query": "Original query text",
  "error_message": "Flutter analysis error message",
  "update_existing": true,
  "session_id": "optional-session-identifier"
}
```

The `update_existing` flag, when set to `true`, will look for the most recent pending generation in the project and update it instead of creating a new one.


### Response Format

The API streams responses in this format:

```json
{
  "type": "Text|Code|Chat|Error|Success|AnalysisError|Result",
  "value": "Message content or object"
}
```

Response types:
- `Text`: Status updates and progress messages
- `Code`: Generated code content
- `Chat`: Conversational explanations and generation plans
- `Error`: Error messages
- `Success`: Success notifications
- `AnalysisError`: Flutter code analysis errors
- `Result`: Final result with URL and file path information

### REST API Endpoints

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

## Architecture

The project follows a clean architecture pattern with these main components:

- `api/` - WebSocket and REST APIs with clean architecture layers
  - `presentation/` - WebSocket handlers and REST controllers
  - `domain/` - Business logic interfaces and use cases
  - `infrastructure/` - Service implementations and data access
- `flutter_generator/` - Core Flutter code generation
  - `core/` - Core generator functionality and LLM integration
  - `config/` - Configuration settings and environment variables
  - `utils/` - Utility functions for code analysis and processing
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
4. Code is analyzed for errors and deployed to the test project
5. The application is built as a web app for immediate preview
6. If errors occur, the service provides detailed feedback for correction

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Ensure the API server is running
   - Check for correct WebSocket endpoint URL
   - Verify network connectivity and firewall settings

2. **Code Generation Errors**
   - Check the error message for specific details
   - Ensure your query is clear and relates to LikeMinds SDK features
   - Use the `FixCode` message type to address specific errors

3. **Flutter Build Errors**
   - Ensure Flutter SDK is correctly installed
   - Check if the generated code is compatible with the current Flutter version
   - Look for detailed error messages in the logs

4. **Authentication Issues**
   - Verify Supabase configuration
   - Ensure your authentication tokens are valid and not expired
   - Check for correct API endpoints and request formats

### Logs and Debugging

- Server logs are available in the `logs/` directory
- Docker logs can be viewed using `docker-compose logs -f`
- For detailed debugging, use the `/api/debug` endpoint (admin access required)

## Deployment

### Production Deployment Recommendations

1. Use Docker Compose for containerized deployment
2. Configure appropriate environment variables for production
3. Set up HTTPS with a valid SSL certificate
4. Configure proper authentication and authorization
5. Set up monitoring and logging solutions
6. Use a reverse proxy like Nginx for production traffic management

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

Copyright LikeMinds, Inc. 