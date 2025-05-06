## Existing Project Support – Detailed Implementation Plan

> Turning imported GitHub repositories into first-class, runnable LikeMinds projects with analysis, generation & preview flows.

### 0. Goals
1. Clone a chosen GitHub repo into the **same on-disk convention** we use for freshly-generated projects.
2. Ingest the cloned source code so Gemini can reason over the **entire project** (contextual code + docs).
3. Provide a **conversation experience** that adapts the prompt if the project is imported (prefix `"GitHub: "`).
4. Re-use/extend the existing code-generation pipeline while feeding the extra context.
5. Add a **RunPreview** WS action so users can run/build the imported/generated project on demand.
6. Refactor toward a more **agentic** architecture (managers/services orchestrating sub-tasks, richer streaming feedback).

---

### 1. Directory Layout
```
output/
└─ {project_id}/
   ├─ generation/            # generated files (CURRENT behaviour)
   └─ integration/           # <– git clone of repo (Currently working as copy of template integration directory)
```
* The **GitHub import service** already creates `{project_id}`; we now additionally:
  * `mkdir -p output/{project_id}/integration`  
  * `git clone --depth=1 {repo_url} output/{project_id}/integration`  
  * Persist the commit SHA for future diff-based updates.
  * Update the existing 'github_repositories' table with the new commit SHA, project_id, and repo_path in our disk.

### 2. Source Ingestion (gitingest)
* Add dependency `gitingest>=0.4` (exact version TBD) in `requirements.txt`.
* New util: `ingest_repo(project_id: str) -> str`  
  1. Run `gitingest output/{project_id}/integration --output output/{project_id}/integration/ingest.txt`  
  2. Return path to `ingest.txt` so downstream components can read it.
* Schedule ingestion **right after clone** and every time the repo is re-imported/refreshed.

### 3. Conversation Layer
#### 3.1 ExistingProjectConversationManager (NEW)
* Mirror `FlutterConversationManager` but:
  * Accept `ingest_text` (loaded from `ingest.txt`).
  * Uses _existing-project-prompt.txt_ (we'll author separately) as the 1st system instruction.
  * Adds a part containing `<project-code>{ingest_text}</project-code>`.
* Exposed via `flutter_generator_service_impl.generate_conversation()` behind a flag `is_imported_project`.

#### 3.2 Prompt Routing Logic
* In `flutter_generator_service_impl` (or higher):
  * `is_imported_project = project.name.startswith("GitHub: ")`  
  * Choose manager: `FlutterConversationManager` vs `ExistingProjectConversationManager`.

### 4. Code Generation Layer
* Extend `FlutterCodeGenerator.generate_code()` to optionally receive:
  * `ingest_text` (string)
  * `is_imported_project` (bool)
* Update `_load_system_instructions()`:
  * When `is_imported_project` is **True** add another `types.Part` with `<project-code>` similar to conversation manager.
* Service signature change (breaking) – update all callers.

### 5. WebSocket Flow Changes
| Msg Type | Purpose | Handler | Notes |
|----------|---------|---------|-------|
| `RunPreview` | Build & run a project (gen or imported) | `_handle_run_preview` (NEW) | Accept `{project_id}`; stream logs back. |

#### 5.1 Implementation Steps
1. Add constant `MSG_RUN_PREVIEW = "RunPreview"` + mapping entry.
2. Handler skeleton:
```py
async def _handle_run_preview(self, ws, msg, ctx):
    project_root = os.path.join("output", ctx["project_id"])
    cmd =  # use our existing command for running the Flutter project
    proc = await asyncio.create_subprocess_exec(*cmd, cwd=project_root,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    async for line in proc.stdout:
        await self.send_json_response(ws, RESP_TEXT, line.decode())
```
3. Respect cancellation on WS disconnect.

### 6. FlutterGeneratorService Enhancements
* When `generate_flutter_code()` detects `is_imported_project`:
  * Ensure ingest exists → pass to generator.
* When **fix code** is requested for imported project, pass ingest as context too.

### 7. Agentic Orchestration
* Replace monolithic calls with **sub-tasks** communicating via the WS stream:
  1. `CloneRepoTask` (if needed)
  2. `IngestTask`
  3. `AnalysisTask` (conversation manager)
  4. `CodeGenTask`
  5. `PreviewTask`
* Each task yields progress events: `{type:"Text", stage:"clone", pct:30}` allowing UI progress bars.

### 8. File & Config Additions
- `existing-project-plan.md` (this file)
- `existing-project-prompt.txt`
- Update `requirements.txt` with `gitingest`.

### 9. Testing Strategy
1. Unit test cloning + ingestion utility (mock git).
2. Unit test prompt routing (project name cases).
3. Integration test: import repo → generate conversation → run preview.
4. E2E via Playwright to cover WebSocket streaming.

### 10. Roll-Out Steps
1. Land utilities & manager classes behind feature flag `ENABLE_IMPORTED_PROJECTS`.
2. Gradually switch GitHub import flow to use new steps.
3. Monitor logs/metrics; add alerting for ingestion/generation failures.

---

## Revised Implementation Approach - Cleaner, More Modular Design

After reviewing our current implementation, I've identified several issues making the code messy:

1. We're adding too many conditionals in existing methods
2. We're mixing project types in the same code paths
3. We're creating tight coupling between the project type detection and the generation logic

Let's revise our approach to be more modular and maintainable:

### 1. Strategy Pattern for Project Types

Instead of adding conditionals throughout the code, we'll implement a **strategy pattern**:

```python
class ProjectHandler:
    """Base class for handling different project types"""
    
    def get_conversation_manager(self, settings):
        """Return the appropriate conversation manager"""
        raise NotImplementedError()
        
    def prepare_code_generation(self, project_id):
        """Prepare for code generation (e.g., get context)"""
        raise NotImplementedError()
        
    def get_generation_context(self, project_id):
        """Get any additional context needed for generation"""
        return {}

class StandardProjectHandler(ProjectHandler):
    """Handler for standard Flutter projects"""
    
    def get_conversation_manager(self, settings):
        return FlutterConversationManager(settings)
        
    def prepare_code_generation(self, project_id):
        return None  # No special context needed
        
class GitHubProjectHandler(ProjectHandler):
    """Handler for GitHub imported projects"""
    
    def get_conversation_manager(self, settings):
        return ExistingProjectConversationManager(settings)
        
    def prepare_code_generation(self, project_id):
        return get_ingest_text(project_id)
        
    def get_generation_context(self, project_id):
        return {
            "is_imported_project": True,
            "ingest_text": get_ingest_text(project_id)
        }
```

### 2. Factory Method for Handler Selection

Add a factory method in the service layer:

```python
def get_project_handler(project_id, access_token):
    """Factory method to get the appropriate project handler"""
    if is_github_project(project_id, access_token):
        return GitHubProjectHandler()
    return StandardProjectHandler()
```

### 3. Simplified Service Layer

Our service methods become much cleaner:

```python
async def generate_conversation(self, user_query, on_chunk, ...):
    # Get the appropriate handler
    handler = self.get_project_handler(project_id, access_token)
    
    # Get the conversation manager from the handler
    conversation_manager = handler.get_conversation_manager(self.settings)
    
    # Use the manager without conditionals
    response = await conversation_manager.generate_conversation(
        user_prompt=user_query,
        project_id=project_id,  # The manager will use this if needed
        on_chunk=on_chunk
    )
    
    # Continue with standard processing...
```

### 4. Configuration-Based Preview Runner

For the RunPreview functionality, create a dedicated class:

```python
class FlutterPreviewRunner:
    """Handles running Flutter previews for any project type"""
    
    def __init__(self, project_id):
        self.project_id = project_id
        
    def find_flutter_directory(self):
        """Find the directory containing the Flutter project"""
        # Logic to check generation/ and integration/ directories
        
    async def run_preview(self, websocket, device="chrome"):
        """Run the Flutter preview and stream output"""
        # Subprocess creation and output streaming
```

### 5. Implementation Plan

1. Create the `ProjectHandler` base class and implementations
2. Add the factory method to get the appropriate handler
3. Update service methods to use the handler pattern
4. Create the `FlutterPreviewRunner` class
5. Update the WebSocket handler to use the runner

This approach:
- Eliminates conditionals by delegating to appropriate handlers
- Makes adding new project types easier (just add a new handler)
- Separates project type detection from business logic
- Creates clearer responsibilities for each component

Let's start by implementing the project handler classes and then refactor the service layer to use them.

## Implementation Task List (New Modular Approach)

### ✅ Completed Tasks

1. ✅ **Module Design and Planning**
   - ✅ Created revised modular design using strategy pattern
   - ✅ Defined clear separation of concerns for different components

2. ✅ **Strategy Pattern Implementation**
   - ✅ Created `ProjectHandler` base class in `flutter_generator/core/project_handler.py`
   - ✅ Implemented `StandardProjectHandler` for new projects
   - ✅ Implemented `GitHubProjectHandler` for GitHub imports

3. ✅ **Factory Pattern Implementation**
   - ✅ Created `ProjectFactory` in `flutter_generator/core/project_factory.py`
   - ✅ Implemented project type detection logic
   - ✅ Added factory method to create appropriate handlers

4. ✅ **Preview Runner Implementation**
   - ✅ Created `FlutterPreviewRunner` in `flutter_generator/core/preview_runner.py`
   - ✅ Implemented directory discovery logic
   - ✅ Added subprocess management and output streaming
   - ✅ Added proper cleanup and cancellation support

5. ✅ **WebSocket Handler Updates**
   - ✅ Updated `_handle_run_preview` to use the new runner class
   - ✅ Added context tracking to the WebSocket handler
   - ✅ Implemented proper cleanup on disconnect

### 🔄 In Progress Tasks

1. 🔄 **Service Layer Refactoring**
   - Refactor `FlutterGeneratorServiceImpl` to use the strategy pattern
   - Remove conditional logic in favor of delegating to handlers
   - Simplify code paths for different project types

### ⏳ Pending Tasks

1. ⏳ **GitHub Import Service Integration**
   - Update to clone repos into the expected directory structure
   - Trigger ingestion after cloning
   - Add support for updating existing repos

2. ⏳ **Testing**
   - Unit tests for new components (handlers, factory, runner)
   - Integration tests for end-to-end flow

3. ⏳ **Documentation**
   - Add class diagrams for the new architecture
   - Update user-facing docs with new features
   - Add contributor docs for the architecture

### 🔄 Next Actions

1. Refactor the `FlutterGeneratorServiceImpl` to use the new strategy pattern:
   - Use `ProjectFactory` to get the appropriate handler
   - Delegate to handler methods rather than using conditionals
   - Simplify the generate_conversation, generate_flutter_code, and fix_flutter_code methods

2. Add a new method to the `FlutterGeneratorServiceImpl` for running previews:
   ```python
   async def run_flutter_preview(
       self,
       user_query: str,
       on_chunk: Callable,
       project_id: str,
       access_token: str = None,
       device: str = "chrome"
   ) -> Dict[str, Any]:
       # Create preview runner and run preview
       ...
   ```

3. Test the new implementation with both standard and GitHub projects. 