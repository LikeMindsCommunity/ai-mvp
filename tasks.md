# Actionable Tasks for Robustness Improvement

This document outlines the key tasks required to address the findings from the technical audit (`audit.md`) and complete the planned features (`auth-ed.md`), aiming for a more robust and production-ready system.

## 1. Authentication & Session Management (Critical Security)

-   **[High] Implement Token Refresh:**
    -   Create `POST /api/auth/refresh` endpoint using `client.auth.refresh_session({'refresh_token': …})`.
    -   Update WebSocket connection logic (`api/presentation/websocket_handler.py`) to handle token expiry and potentially use refresh tokens or trigger reconnection.
    -   Update client-side (`integration_tester.html` or equivalent) to store refresh tokens securely and call the refresh endpoint.
-   **[Medium] Implement Full Logout:**
    -   Investigate using Supabase Admin API (or future Management API) to revoke refresh tokens server-side on logout (`POST /api/auth/logout`).
    -   If not feasible, clearly document that logout is best-effort client-side session clearing.
-   **[Low] Fix Swagger UI Auth Path:**
    -   In `api/infrastructure/auth/jwt.py`, change `OAuth2PasswordBearer(tokenUrl="/api/auth/login")` to `OAuth2PasswordBearer(tokenUrl="/api/auth/login/oauth")` or add an alias route.
-   **[Medium] Implement Password Management:**
    -   Implement `POST /api/auth/reset-password` (request flow, likely needs email service integration).
    -   Implement `POST /api/auth/change-password` (authenticated flow).

## 2. Database, Migrations & RLS (Critical Security & Stability)

-   **[High] Implement RLS Policies:**
    -   Create SQL migration files (e.g., in `supabase/migrations/`) for all tables (`projects`, `code_generations`, `project_members` etc.).
    -   Define strict RLS policies for SELECT, INSERT, UPDATE, DELETE on `projects` ensuring users can only access projects they own or are members of.
    -   Define RLS policies for `code_generations` ensuring users can only access/modify records linked to projects they have access to.
    -   Define RLS policies for `project_members`.
    -   Enable RLS on all relevant tables in Supabase.
-   **[High] Setup Migration Management:**
    -   Integrate `supabase/cli` into the development workflow.
    -   Use `supabase db diff` to generate migration files for schema changes.
    -   Establish a process for applying migrations (local dev, staging, production).
    -   Add a CI check to ensure migrations are up-to-date.
-   **[Medium] Add Database Indices:**
    -   Create migrations to add indices on foreign key columns like `code_generations.project_id`, `code_generations.user_id`, `project_members.project_id`, `project_members.user_id`.
-   **[Low] Refine `code_generations.status`:**
    -   Consider using a Postgres `ENUM` type for the `status` column (`pending`, `running`, `completed`, `error`, `cancelled`).
    -   Add a `CHECK` constraint or use the `ENUM` type to enforce valid status values.

## 3. Code Generation & Execution (Critical Stability & Scalability)

-   **[High] Isolate Integration Environment:**
    -   Modify `FlutterCodeManager` and `FlutterIntegrationManager` to work within per-generation temporary directories (e.g., `output/<project_id>/<generation_id>/integration/`).
    -   Ensure the `integration/` directory in the root is treated only as a template.
    -   Update `FlutterGeneratorServiceImpl` to manage these temporary directories.
-   **[High] Offload Long-Running Tasks:**
    -   Introduce a background task queue (e.g., Celery + Redis/RabbitMQ, Arq, RQ).
    -   Refactor `FlutterGeneratorServiceImpl.generate_flutter_code` and `fix_flutter_code`:
        -   The API call should enqueue a task with `project_id`, `generation_id`, `user_query`, etc.
        -   The task worker will perform Gemini calls, file operations, `flutter pub get`, `flutter analyze`, and potentially `flutter run`.
    -   Update `code_generations` table to include `task_id` or `queue_id`.
    -   Change WebSocket communication:
        -   The handler should return immediately after queueing the task.
        -   The client polls for status updates (via REST or another WebSocket message) or the backend uses Server-Sent Events (SSE) / PubSub (like Redis PubSub or Supabase Realtime) to push status updates based on the `generation_id`.
-   **[High] Implement WebSocket Cleanup:**
    -   In `WebSocketHandler`, modify the `except WebSocketDisconnect:` block.
    -   Implement logic to signal cancellation to the background task (if possible) or at least mark the `code_generations` record as `cancelled`.
    -   Ensure any running `FlutterIntegrationManager` processes (`flutter run`) associated with the disconnected session are properly terminated (`stop_flutter_app`).
    -   Clean up temporary directories associated with the cancelled generation.
-   **[Medium] Optimize Command Output Handling:**
    -   Refactor `FlutterIntegrationManager.run_command_with_timeout` and `_read_process_output`.
    -   Instead of buffering all output in memory, stream relevant lines/chunks directly to the client via the chosen status update mechanism (WebSocket/SSE/PubSub).
    -   Keep only a small rolling buffer in memory if needed for context/error reporting.
-   **[Medium] Persist Conversation History:**
    -   Remove the in-memory `self.conversation_history` from `FlutterGeneratorServiceImpl`.
    -   Create a new Supabase table (e.g., `conversation_history` with `project_id`, `session_id` or `user_id`, `messages_jsonb`, `timestamp`).
    -   Alternatively, use Redis (HASH or LIST) with a TTL keyed by `project_id:session_id`.
    -   Update `_update_conversation_history` and generation methods to read/write history from the persistent store.

## 4. Project Management & Authorization (Critical Security)

-   **[High] Implement Project Access Control:**
    -   In `api/presentation/projects.py` and `api/infrastructure/projects/service.py`, ensure *every* endpoint rigorously checks project ownership/membership based on the authenticated user (`auth.uid()`) and RLS (once implemented). Do not rely solely on RLS; add application-level checks too.
    -   In `api/presentation/websocket_handler.py`, before processing *any* message (`GenerateCode`, `FixCode`, etc.), verify that the authenticated `user` has access to the provided `project_id` by calling `service.get_project`.
-   **[Medium] Implement Project Sharing:**
    -   Fully implement the logic for `POST /api/projects/{project_id}/share` in `api/infrastructure/projects/service.py`.
    -   This should add entries to the `project_members` table.
    -   Ensure only project owners can share.
    -   Implement corresponding `DELETE /api/projects/{project_id}/unshare` or similar endpoint.

## 5. Observability & Operations

-   **[Medium] Implement Structured Logging:**
    -   Replace all `print()` statements with a proper logging library (e.g., `loguru` or standard `logging`).
    -   Configure structured logging (e.g., JSON format).
    -   Include contextual information in logs (e.g., `request_id`, `user_id`, `project_id`, `generation_id`).
    -   Add logging middleware to FastAPI (`api/main.py`).
-   **[Medium] Improve Flutter Process Health Check:**
    -   In `FlutterIntegrationManager`, enhance the monitoring of the `flutter run` process.
    -   Consider adding more robust checks beyond the HTTP ping, potentially monitoring the process state directly or adding specific log messages to watch for.
    -   Implement basic restart logic or clearer error reporting if the Dart process crashes.
-   **[Low] Add `.env.example`:**
    -   Create a `.env.example` file listing all required environment variables with placeholder values or descriptions.

## 6. Testing & CI

-   **[Medium] Add Unit & Integration Tests:**
    -   Write unit tests for core logic in `infrastructure/services`, `flutter_generator/core`. Mock external dependencies (Gemini API, Supabase client, `subprocess`).
    -   Write integration tests using `pytest-asyncio` and `httpx` for API endpoints (Auth, Projects).
    -   Write tests for the WebSocket handler (`test_websocket_client`).
-   **[Medium] Setup CI Pipeline:**
    -   Configure a CI pipeline (e.g., GitHub Actions) to run linters (`ruff`, `black`), type checks (`mypy`), and tests on every push/PR.
    -   Include a step to check Supabase schema drift (`supabase db diff --check`).

## 7. Configuration & Code Quality

-   **[Low] Remove Unused JWT Secret:**
    -   Remove `jwt_secret`, `jwt_algorithm`, `access_token_expire_minutes` from `api/config.py::Settings` as Supabase handles JWT signing/verification.
    -   Remove the `create_access_token` function from `api/infrastructure/auth/jwt.py` if it's not used elsewhere.
-   **[Low] Formalize WebSocket Event Schema:**
    -   Define Pydantic models for all outbound WebSocket message types (`Text`, `Code`, `Chat`, `Error`, `AnalysisError`, `Result`, `StatusUpdate`).
    -   Use `model_dump()` in `WebSocketHandler.on_chunk` (or equivalent) to ensure consistent serialization.
-   **[Low] Improve WebSocket Chunking:**
    -   In `WebSocketHandler.on_chunk` (or equivalent status sender), implement logic to slice large `Code` chunks to prevent potentially overwhelming the client connection or browser rendering.

## 8. GitHub Repository Integration (Enhancement)

-   **[High] OAuth Linking of GitHub Accounts:**
    -   Extend the auth module to allow users to connect their GitHub account via existing OAuth (`api/auth/github`).
    -   Persist GitHub access tokens securely (e.g., encrypted in database) associated with user.
    -   Update the oAuth flow to use Github App installation.
-   **[High] List and Select Repositories:**
    -   Add endpoint `GET /api/repos` that uses the stored GitHub token to fetch and return a list of user repositories.
    -   Add endpoint `POST /api/repos/import` to select a repository, specify branch/folder, and enqueue import.
-   **[High] Clone and Prepare Repository Workspace:**
    -   Implement a service (`GitHubRepoService`) that clones the selected repository into a temporary workspace directory (e.g., `output/<project_id>/<generation_id>/repos/`).
    -   Detect Flutter projects by scanning for `pubspec.yaml` files and present available entry paths for integration.
    -   Prepare a flat summary `codebase.txt` using gitingest of the project codebase for us to analyse the query and see how to generate the best code.
    -   Ensure clones are shallow (single branch) and cleaned up after use or cancellation.
-   **[Medium] Integrate Code Generation into Existing Codebase:**
    -   Refactor `FlutterGeneratorServiceImpl` (or its background task) to accept a `repo_path` parameter and use the flat `codebase.txt` summary to generate the best code.
    -   apply generated changes directly into the repo's `lib/` folder or user-specified target.
    -   Support previewing diffs and choosing insertion points (e.g., via PR on a branch).
    -   After generation, commit changes back to a new Git branch and push to the user's GitHub repository if authorized.
-   **[Medium] Provide Feedback and Cleanup:**
    -   Stream status updates during clone, code generation, and commit phases back to the client via WebSocket/SSE.
    -   Implement cleanup of cloned repositories and branches on success, failure, or user cancellation.
    -   Record import and integration metadata in Supabase (e.g., `repo_imports` table with `status`, `url`, `branch`).

---

*Assign priorities (High, Medium, Low) and track progress using checkboxes.* 