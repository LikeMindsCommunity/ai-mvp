# Comprehensive Task List

## 1. Authentication & Session Management

### 1.1 Implement Token Refresh [High]
- [x] Create `POST /api/auth/refresh` endpoint
  - [x] Define route in FastAPI
  - [x] Implement controller logic using Supabase client.auth.refresh_session
  - [x] Add request validation with Pydantic model
  - [x] Add error handling for invalid/expired tokens
  - [x] Write documentation for the endpoint
- [x] Update WebSocket connection logic
  - [x] Modify `api/presentation/websocket_handler.py` to detect token expiry
  - [x] Implement reconnection or refresh token mechanism
  - [x] Add error handlers for authentication failures
- [x] Update client-side implementation
  - [x] Add secure storage for refresh tokens
  - [x] Implement client-side token refresh logic
  - [x] Add automatic retry for failed requests due to token expiry

### 1.2 Implement Full Logout [Medium]
- [x] Research Supabase Admin API for token revocation
  - [x] Document findings on feasibility
  - [x] Determine if Management API is needed
- [x] Implement server-side logout endpoint
  - [x] Create `POST /api/auth/logout` route
  - [x] Add logic for revoking refresh tokens if possible
  - [x] Implement client-session clearing as fallback
- [x] Update documentation
  - [x] Document logout limitations if server-side revocation isn't possible
  - [x] Add security recommendations for users

### 1.3 Fix Swagger UI Auth Path [Low]
- [x] Update OAuth2PasswordBearer configuration
  - [x] In `api/infrastructure/auth/jwt.py`, change tokenUrl to correct path
  - [x] Test Swagger UI authentication flow
- [x] Consider adding alias route if needed
  - [x] Implement alias in FastAPI router

### 1.4 Implement Password Management [Medium]
- [x] Create password reset request flow
  - [x] Implement `POST /api/auth/reset-password` endpoint
  - [x] Research email service integration options
  - [x] Implement email sending for reset links
  - [x] Create token generation for reset links
  - [x] Add validation for reset tokens
- [x] Implement password change flow
  - [x] Create `POST /api/auth/change-password` endpoint
  - [x] Add authentication requirement
  - [x] Implement password validation logic
  - [x] Add confirmation step for security

## 2. Database, Migrations & RLS

### 2.1 Implement RLS Policies [High]
- [ ] Set up migration directory
  - [ ] Create `supabase/migrations/` structure if not exists
  - [ ] Research best practices for Supabase migrations
- [ ] Create RLS policies for `projects` table
  - [ ] Define SELECT policy (owner or member access only)
  - [ ] Define INSERT policy (authenticated users only)
  - [ ] Define UPDATE policy (owner only or specified permissions)
  - [ ] Define DELETE policy (owner only)
  - [ ] Write migration file for projects table RLS
- [ ] Create RLS policies for `code_generations` table
  - [ ] Define SELECT policy (linked to accessible projects only)
  - [ ] Define INSERT policy (linked to accessible projects only)
  - [ ] Define UPDATE policy (linked to accessible projects only)
  - [ ] Define DELETE policy (linked to accessible projects only)
  - [ ] Write migration file for code_generations table RLS
- [ ] Create RLS policies for `project_members` table
  - [ ] Define SELECT policy (visible to project owners and members)
  - [ ] Define INSERT policy (project owners only)
  - [ ] Define UPDATE policy (project owners only)
  - [ ] Define DELETE policy (project owners only)
  - [ ] Write migration file for project_members table RLS
- [ ] Enable RLS on all tables
  - [ ] Create migration to enable RLS for all tables
  - [ ] Test RLS policies thoroughly

### 2.2 Setup Migration Management [High]
- [ ] Install and configure Supabase CLI
  - [ ] Add to development dependencies
  - [ ] Create configuration files
  - [ ] Document CLI usage for team
- [ ] Implement migration generation process
  - [ ] Document how to use `supabase db diff`
  - [ ] Create template for migration files
- [ ] Establish migration application process
  - [ ] Document local development migration procedure
  - [ ] Document staging environment migration procedure
  - [ ] Document production migration procedure
  - [ ] Create migration scripts if needed
- [ ] Add CI checks for migrations
  - [ ] Create GitHub Action or similar CI step
  - [ ] Implement check for uncommitted schema changes

### 2.3 Add Database Indices [Medium]
- [ ] Analyze query patterns
  - [ ] Review existing queries for performance bottlenecks
  - [ ] Identify frequently accessed columns
- [ ] Create index migrations
  - [ ] Add index for `code_generations.project_id`
  - [ ] Add index for `code_generations.user_id`
  - [ ] Add index for `project_members.project_id`
  - [ ] Add index for `project_members.user_id`
  - [ ] Add any other indices identified during analysis
- [ ] Test query performance
  - [ ] Benchmark queries before and after index creation
  - [ ] Document performance improvements

### 2.4 Refine `code_generations.status` [Low]
- [ ] Evaluate ENUM approach
  - [ ] Research Postgres ENUM type implementation
  - [ ] List all possible status values
- [ ] Implement chosen approach
  - [ ] Create migration for ENUM type creation if chosen
  - [ ] OR create migration for CHECK constraint
  - [ ] Update corresponding code in services
- [ ] Migrate existing data
  - [ ] Handle transition of existing records
  - [ ] Validate data integrity after migration

## 3. Code Generation & Execution

### 3.1 Isolate Integration Environment [High]
- [x] Design directory structure
  - [x] Define path pattern for per-generation directories
  - [x] Document directory lifecycle management
- [x] Modify `FlutterCodeManager`
  - [x] Update to use per-generation directories
  - [x] Add utility methods for directory management
  - [x] Ensure proper cleanup on completion/failure
- [x] Modify `FlutterIntegrationManager`
  - [x] Update to work with isolated directories
  - [x] Adapt command execution for new paths
  - [x] Handle path resolution correctly
- [x] Update root `integration/` directory handling
  - [x] Convert to template-only usage
  - [x] Implement copying mechanism to temporary directories
- [x] Update `FlutterGeneratorServiceImpl`
  - [x] Modify to create and manage temporary directories
  - [x] Add cleanup methods
  - [x] Implement directory tracking

### 3.2 Optimize Project Directory Structure [High]
- [x] Implement project-based organization
  - [x] Create separate directory for each project
  - [x] Store all generations for a project in one location
  - [x] Reuse integration environment for each project
- [x] Update WebSocket handler
  - [x] Track projects instead of individual generations
  - [x] Update cleanup logic for project-based structure
  - [x] Ensure proper "Result" response formatting for frontend compatibility
- [x] Update service implementation
  - [x] Modify managers to work with project IDs
  - [x] Update interface to include project_id parameter
  - [x] Implement cleanup at project level instead of generation level

### 3.3 Offload Long-Running Tasks [High]
- [ ] Research and select background task queue
  - [ ] Evaluate Celery + Redis/RabbitMQ
  - [ ] Evaluate Arq
  - [ ] Evaluate RQ
  - [ ] Document selection rationale
- [ ] Set up task queue infrastructure
  - [ ] Install required dependencies
  - [ ] Configure message broker
  - [ ] Set up worker processes
  - [ ] Create deployment documentation
- [ ] Refactor code generation service
  - [ ] Extract `generate_flutter_code` to task
  - [ ] Extract `fix_flutter_code` to task
  - [ ] Create task invocation from API endpoint
  - [ ] Add task tracking and result handling
- [ ] Update database schema
  - [ ] Add `task_id` or `queue_id` to `code_generations` table
  - [ ] Create migration file
- [ ] Implement status update mechanism
  - [ ] Design polling API or
  - [ ] Implement SSE endpoint or
  - [ ] Set up PubSub with Supabase Realtime
  - [ ] Update client-side code to handle updates

### 3.4 Implement WebSocket Cleanup [High]
- [ ] Enhance disconnect handler
  - [ ] Modify `WebSocketHandler` exception block
  - [ ] Add cancellation signal to background tasks
  - [ ] Update `code_generations` status on disconnect
- [ ] Implement process termination
  - [ ] Ensure `flutter run` processes are properly stopped
  - [ ] Add process tracking mechanism
  - [ ] Test graceful and forceful termination paths
- [ ] Add directory cleanup
  - [ ] Implement temporary directory removal
  - [ ] Add safety checks for path validation
  - [ ] Test cleanup process thoroughly

### 3.5 Optimize Command Output Handling [Medium]
- [ ] Refactor output handling methods
  - [ ] Update `run_command_with_timeout` function
  - [ ] Modify `_read_process_output` function
- [ ] Implement streaming output
  - [ ] Replace in-memory buffering with streaming
  - [ ] Define chunking strategy for output
  - [ ] Update WebSocket/SSE handler to stream chunks
- [ ] Implement rolling buffer
  - [ ] Create configurable buffer size for context
  - [ ] Add logic to maintain recent output for error reporting
  - [ ] Test memory usage under load

### 3.6 Persist Conversation History [Medium]
- [x] Remove in-memory conversation history
  - [x] Identify all uses of `self.conversation_history`
  - [x] Plan replacement strategy
- [x] Design persistence solution
  - [x] Create function to fetch project conversations from Supabase
  - [x] Implement history loading when starting a WebSocket session
  - [x] Add API for retrieving conversation history
- [x] Implement client-side integration
  - [x] Update frontend to fetch conversation history on connection
  - [x] Display previous conversations in chat interface
  - [x] Add UI components for conversation history

## 4. Project Management & Authorization

### 4.1 Implement Project Access Control [High]
- [ ] Audit current access control
  - [ ] Review all project-related endpoints
  - [ ] Identify authorization gaps
- [ ] Enhance `api/presentation/projects.py`
  - [ ] Add explicit ownership/membership checks
  - [ ] Add user authorization to all routes
  - [ ] Ensure consistent error responses
- [ ] Enhance `api/infrastructure/projects/service.py`
  - [ ] Add access control helper methods
  - [ ] Implement authorization for all service methods
- [ ] Secure WebSocket handler
  - [ ] Update `api/presentation/websocket_handler.py`
  - [ ] Add project access verification
  - [ ] Implement project ownership checks
  - [ ] Add comprehensive error handling

### 4.2 Implement Project Sharing [Medium]
- [ ] Complete sharing endpoint implementation
  - [ ] Implement logic for `POST /api/projects/{project_id}/share`
  - [ ] Add validation for owner-only access
  - [ ] Implement `project_members` table operations
- [ ] Create unshare functionality
  - [ ] Implement `DELETE /api/projects/{project_id}/unshare` endpoint
  - [ ] Add validation for owner-only access
  - [ ] Implement member removal logic
- [ ] Add sharing management features
  - [ ] Create endpoint to list project members
  - [ ] Add endpoint to change member permissions (if applicable)

## 5. Observability & Operations

### 5.1 Implement Structured Logging [Medium]
- [ ] Select logging library
  - [ ] Evaluate loguru
  - [ ] Evaluate standard logging module
  - [ ] Document selection rationale
- [ ] Replace print statements
  - [ ] Search codebase for print() calls
  - [ ] Replace with appropriate logging calls
  - [ ] Add context information to log messages
- [ ] Configure structured logging
  - [ ] Set up JSON formatter
  - [ ] Configure log levels
  - [ ] Add log file rotation if needed
- [ ] Add FastAPI logging middleware
  - [ ] Implement in `api/main.py`
  - [ ] Add request/response logging
  - [ ] Include performance metrics

### 5.2 Improve Flutter Process Health Check [Medium]
- [ ] Enhance monitoring
  - [ ] Improve HTTP ping mechanism
  - [ ] Add direct process state monitoring
  - [ ] Implement log scanning for critical errors
- [ ] Add robustness to `FlutterIntegrationManager`
  - [ ] Implement more comprehensive health checks
  - [ ] Add periodic verification
- [ ] Implement recovery procedures
  - [ ] Add restart logic for crashed processes
  - [ ] Improve error reporting
  - [ ] Document recovery procedures

### 5.3 Add `.env.example` [Low]
- [ ] Create `.env.example` file
  - [ ] List all required environment variables
  - [ ] Add descriptions and example values
  - [ ] Document usage in README
- [ ] Update documentation
  - [ ] Add environment setup instructions
  - [ ] Document variable requirements

## 6. Testing & CI

### 6.1 Add Unit & Integration Tests [Medium]
- [ ] Set up testing framework
  - [ ] Add pytest configuration
  - [ ] Configure test directories
  - [ ] Add test dependencies
- [ ] Write unit tests
  - [ ] Test core logic in `infrastructure/services`
  - [ ] Test `flutter_generator/core` functionality
  - [ ] Create mocks for external dependencies
- [ ] Write integration tests
  - [ ] Set up `pytest-asyncio` and `httpx`
  - [ ] Test authentication endpoints
  - [ ] Test project management endpoints
- [ ] Create WebSocket tests
  - [ ] Implement `test_websocket_client`
  - [ ] Test message handling
  - [ ] Test disconnect scenarios

### 6.2 Setup CI Pipeline [Medium]
- [ ] Configure CI platform
  - [ ] Set up GitHub Actions or alternative
  - [ ] Define CI workflow
- [ ] Add linting checks
  - [ ] Configure ruff
  - [ ] Configure black
  - [ ] Add linting job to CI
- [ ] Add type checking
  - [ ] Configure mypy
  - [ ] Add type checking job to CI
- [ ] Add test execution
  - [ ] Configure test runner in CI
  - [ ] Set up test reporting
- [ ] Add schema drift check
  - [ ] Implement `supabase db diff --check` step
  - [ ] Document resolution procedure for failures

## 7. Configuration & Code Quality

### 7.1 Remove Unused JWT Secret [Low]
- [ ] Audit JWT usage
  - [ ] Verify Supabase handles all JWT operations
  - [ ] Check for any custom JWT usage
- [ ] Update configuration
  - [ ] Remove `jwt_secret` from `api/config.py::Settings`
  - [ ] Remove `jwt_algorithm`
  - [ ] Remove `access_token_expire_minutes`
- [ ] Clean up unused code
  - [ ] Remove `create_access_token` if unused
  - [ ] Update any dependent code

### 7.2 Formalize WebSocket Event Schema [Low]
- [ ] Define Pydantic models
  - [ ] Create model for `Text` messages
  - [ ] Create model for `Code` messages
  - [ ] Create model for `Chat` messages
  - [ ] Create model for `Error` messages
  - [ ] Create model for `AnalysisError` messages
  - [ ] Create model for `Result` messages