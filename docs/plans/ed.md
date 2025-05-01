# System Overview: LikeMinds Flutter Integration Assistant

## 1. Introduction & Purpose

The **LikeMinds Flutter Integration Assistant** is an AI-powered backend service and development tool designed to streamline the process of integrating LikeMinds Chat and Feed SDKs (and potentially other libraries) into Flutter applications. Its primary goal is to:

- **Accelerate Development:** Reduce the time and effort required for developers to implement common LikeMinds SDK features by providing ready-to-use, validated code snippets and integration examples.
- **Improve Accuracy:** Leverage AI (Google's Gemini 2.5 Pro) to generate correct and idiomatic Flutter/Dart code based on natural language prompts or specific integration requirements.
- **Provide Real-time Feedback:** Offer immediate code analysis, error detection, and a live testing environment to ensure generated integrations work as expected.
- **Support Multi-User Workflows:** Enable multiple developers to use the system securely, managing their own integration projects and sessions.

In essence, it acts as an intelligent assistant that developers can interact with via a WebSocket API to describe their integration needs, receive generated code, test it, and iterate until the integration is successful.

---

## 2. Core Functionality & Features

The system offers the following key features:

- **AI-Powered Code Generation:** Accepts user prompts (e.g., "Create a Flutter chat screen using LikeMinds SDK") and uses the Gemini API to generate relevant Dart code.
- **WebSocket API:** Provides the primary interface for interaction, allowing real-time streaming of:
    - Status updates and progress messages (`Text`).
    - Generated code blocks (`Code`).
    - Conversational explanations and generation plans (`Chat`).
    - System errors (`Error`).
    - Success notifications (`Success`).
    - Flutter code analysis errors (`AnalysisError`).
    - Final results including URLs and file paths (`Result`).
- **Real-time Code Analysis:** Automatically runs `flutter analyze` on generated code to detect syntax errors, warnings, and potential issues.
- **Integration Testing Environment:** Deploys generated code into a pre-configured Flutter test project (`integration/`) for multiple platforms (Linux, macOS, Windows).
- **Live Preview (Web Build):** Can build and host a web version of the integrated Flutter app for quick visual verification.
- **Interactive Error Handling:** Allows users to provide error messages from analysis or runtime, prompting the AI to attempt fixes (`FixCode` type).
- **Authentication & Authorization:** Secure user registration and login using JWT, ensuring only authorized users can access the system.
- **Session Management:** Tracks user sessions, allowing secure access across requests and session invalidation (logout).
- **Project Management:** Enables users to create, manage, and isolate different integration efforts within named projects. All generated artifacts and state are scoped to a project.
- **Conversation History:** (Optional, via `session_id` in WebSocket) Maintains context across multiple requests within a session/project.

---

## 3. High-Level Workflow

A typical interaction with the system follows these steps:

1.  **Authentication:**
    - A developer registers or logs in via the REST API (`/api/auth/login`), receiving JWT access and refresh tokens.
2.  **Project Selection/Creation:**
    - The developer lists their existing projects (`GET /api/projects/`) or creates a new one (`POST /api/projects/`).
3.  **WebSocket Connection:**
    - The developer establishes a WebSocket connection to `ws://host:port/api/flutter`, passing the JWT token and the selected `project_id` for authorization and context.
4.  **Integration Request:**
    - The developer sends a message via WebSocket (e.g., `type: GenerateCode`, `user_query: "..."`).
5.  **Backend Processing:**
    - The backend validates the request and session.
    - It interacts with the Gemini API, providing context (project details, conversation history, SDK docs).
    - It streams back explanations, code snippets, and status updates.
6.  **Code Generation & Analysis:**
    - Generated Dart code is received by the backend.
    - The code is saved (e.g., `output/project_xyz/flutter_code_1.dart`).
    - It's copied into the `integration/lib/main.dart` file for the specific project context.
    - `flutter analyze` is run within the `integration/` directory.
    - Analysis results (success or errors) are streamed back.
7.  **Testing & Verification (Optional):**
    - The backend can trigger a build (e.g., `flutter build web`) within the `integration/` directory.
    - A URL to the live web preview might be provided.
8.  **Iteration:**
    - If errors occur or modifications are needed, the developer can send follow-up messages (`FixCode` or new `GenerateCode` prompts).
9.  **Project Management:**
    - The developer can switch projects, update project details, or delete projects via the REST API.
10. **Logout:**
    - The developer can explicitly log out (`POST /api/auth/logout`), invalidating the session.

---

## 4. Architecture & Key Components

The system employs a clean architecture pattern, primarily within the `api/` directory, separating concerns into distinct layers and modules.

-   **`api/`**: The main backend application (FastAPI).
    -   **`presentation/`**: Handles incoming requests and outgoing responses.
        -   `websocket_handler.py`: Manages WebSocket connections and message routing.
        -   `auth.py`, `users.py`, `sessions.py`, `projects.py`: REST API endpoint definitions (routers) for the new features.
        -   `main.py`: FastAPI application setup, middleware, and mounting routers.
    -   **`domain/`**: Contains core business logic, interfaces, and domain models.
        -   Subdirectories (`auth/`, `users/`, `sessions/`, `projects/`, potentially `generation/`) define interfaces (abstract base classes or protocols) and Pydantic models representing core entities.
    -   **`infrastructure/`**: Provides concrete implementations for domain interfaces.
        -   `services/`: Implementations for interacting with external systems (Gemini API, database, file system, Flutter CLI).
        -   Subdirectories (`auth/`, `users/`, `sessions/`, `projects/`) contain service implementations for the respective domains (e.g., `JWTService`, `UserService`, `ProjectRepository`).
        -   (Potential) `persistence/`: Database interaction logic (e.g., using SQLAlchemy or an ORM).
-   **`flutter_generator/`**: Python utilities specifically for Flutter/Dart code handling.
    -   `core/`: Classes like `FlutterCodeManager`, `FlutterCodeGenerator`, `FlutterIntegrationManager` handling code extraction, saving, analysis, and integration project manipulation.
    -   `config/`: Configuration settings (potentially merged/replaced by central config).
    -   `utils/`: Helper functions.
-   **`integration/`**: A template Flutter project.
    -   Contains `lib/main.dart` (which gets overwritten with generated code).
    -   Platform-specific runner directories (`linux/`, `macos/`, `windows/`, `web/`).
    -   Used as the environment for `flutter analyze` and `flutter build`.
-   **`output/`**: Directory where generated artifacts (e.g., `.dart` files) are stored, likely organized by project ID.
-   **`run_server.py`**: Entry point script to start the Uvicorn server hosting the FastAPI app.
-   **`agent.py`**: (May be refactored/integrated) Contains higher-level orchestration logic, potentially becoming part of the `infrastructure/services/` or `domain/` layers.
-   **`ARCHITECTURE_AUTH_PROJECT_MANAGEMENT.md`**: Planning document for auth/project features.
-   **`README.md`**: Project overview, setup, and basic usage.
-   **`docs.txt`, `code.txt`**: Large text files likely containing SDK documentation or code context used for the AI prompt.

---

## 5. Technology Stack

-   **Backend Language:** Python 3.x
-   **Web Framework:** FastAPI
-   **ASGI Server:** Uvicorn
-   **WebSocket Library:** FastAPI WebSockets
-   **AI:** Google Gemini API (via appropriate Python client library)
-   **Authentication:** JWT (via `python-jose` or similar)
-   **Password Hashing:** bcrypt / argon2
-   **Data Validation:** Pydantic
-   **Target Platform:** Flutter SDK
-   **Process Management:** Python `subprocess` module
-   **Potential Database:** PostgreSQL/SQLite (via SQLAlchemy or other ORM) - *if persistence beyond filesystem is added*
-   **Potential Caching/Session Store:** Redis - *if scalable session management is needed*

---

## 6. Intended Users

-   **Flutter Developers:** Anyone building Flutter applications who needs to integrate LikeMinds SDKs or potentially other complex libraries.
-   **LikeMinds Internal Teams:** For testing SDK integrations, generating documentation examples, and potentially providing developer support.

---

## 7. Conclusion

The LikeMinds Flutter Integration Assistant is a sophisticated tool aimed at significantly improving the developer experience when working with LikeMinds SDKs in Flutter. By combining AI-driven code generation with real-time analysis, testing, and robust project/user management, it provides a powerful, secure, and efficient platform for building integrations. 