**1. Introduction & Goals**

- **1.1. Purpose:** The `agent_system` module will be the new intelligent core of the LikeMinds Flutter Integration Assistant. It replaces the existing `flutter_generator` module with a robust, performant, and modular multi-agent system based on the Agno framework.

- **1.2. Key Objectives:**
    - Implement a flexible agentic architecture capable of handling complex Flutter integration tasks.
    - Integrate Retrieval Augmented Generation (RAG) for contextually aware and accurate assistance.
    - Ensure modularity for easier development, testing, and future extensions of agent capabilities.
    - Improve performance and robustness through asynchronous processing and clear error handling.
    - Provide a seamless integration with the existing FastAPI API layer with minimal disruption to external contracts.
    - Leverage the Agno framework for defining, running, and potentially deploying agentic components.

**2. High-Level Architecture**

- **2.1. System Diagram:**

- **2.2. Agno Framework Role:**
    - Specialized agents (Research, Analysis, etc.) will be implemented as Agno applications or tasks, leveraging Agno's Pythonic interface for defining logic.
    - Agno will be used to run these agent tasks. Its deployment features will be evaluated for scaling individual agents.
    - If Agno provides tool abstractions, they will be used; otherwise, agents will use Python's native capabilities (`subprocess`, `httpx`) for external tool calls.
- **2.3. Interaction with `api` Module:**
    - The `api/presentation/websocket_handler.py` will call methods on `AgnoAgenticFlutterServiceImpl`.
    - This service acts as a facade, translating API requests into tasks for the `agent_system.OrchestratorAgent`.
    - It uses an `asyncio.Queue` per request to bridge the asynchronous agent outputs back to the WebSocket's `on_chunk` callback, maintaining the existing streaming behavior for the client.
- **2.4. External Services:**
    - LLMs (Google Gemini via Python SDK).
    - Supabase (for auth, project data, RAG metadata, agent task state).
    - Vector Database (e.g., ChromaDB, pgvector) for RAG.
    - Flutter CLI, Git CLI.

**3. Core Components (Specialized Agents)**

- **3.1. Orchestrator Agent (`agent_system/orchestrator.py`)**
    - **Purpose:** Central coordinator of the specialized agents.
    - **Responsibilities:**
        - Receives task requests (including a response queue/channel info) from `AgnoAgenticFlutterServiceImpl`.
        - Manages the lifecycle of an integration task (e.g., "GenerateCode", "FixCode").
        - Sequences calls to specialized agents based on the task type and current state.
        - Passes data (Plan Document, PRD, code artifacts, error reports) between agents.
        - Handles errors from agents and decides on retry/fallback or reporting failure.
        - Posts status updates, intermediate results, and final results to the provided response queue.
    - **Primary Inputs:** Task details (operation type, user query, project context, `db_generation_id`), response queue/channel.
    - **Primary Outputs:** Streams messages to the response queue; final success/failure status.
    - **Agno Task Structure:** Could be a main Agno application or a complex Python class that invokes other Agno tasks. Its `process_request` method will be the entry point.
- **3.2. Research Agent (`agent_system/research_agent/`)**
    - **Purpose:** Understand user's request, gather initial context, and formulate a high-level plan.
    - **Responsibilities:** Parse query, high-level analysis of user's codebase (if existing project, via `ingest.txt`), high-level SDK feature mapping.
    - **Inputs:** User query, `project_id`, (optional) codebase summary.
    - **Outputs:** "Plan Document" (structured text/JSON: goal, SDK features, relevant user code areas, high-level steps).
    - **Tools:** LLM, file system access (for `ingest.txt`), basic RAG on SDK overview.
    - **Agno Task Structure:** An Agno task taking query/context, returning the Plan Document.
- **3.3. Analysis Agent (`agent_system/analysis_agent/`)**
    - **Purpose:** Deep technical analysis based on the "Plan Document" to produce a detailed PRD for generation.
    - **Responsibilities:** Detailed RAG on SDK docs/examples, targeted analysis of user's codebase, identify integration points, configs, required code, dependencies.
    - **Inputs:** "Plan Document", full SDK docs, SDK examples, user's codebase (`ingest.txt` or specific files).
    - **Outputs:** "Product Requirements Document (PRD)" (structured: files to change, APIs, dependencies, configs).
    - **Tools:** Advanced RAG (semantic/hybrid search, re-ranking), LLM for synthesis, potentially code parsing tools.
    - **Agno Task Structure:** An Agno task taking Plan Doc and context, returning the PRD.
- **3.4. Generator Agent (`agent_system/generator_agent/`)**
    - **Purpose:** Generate Flutter/Dart code according to the PRD.
    - **Responsibilities:** Implement PRD specs, generate new files, generate modifications for existing files, adhere to multi-file format. Relies primarily on PRD, with docs/code as backup reference.
    - **Inputs:** "PRD", (backup) SDK docs/code.
    - **Outputs:** Structured code operations (list of files with full content, `pubspec.yaml` changes).
    - **Tools:** LLM (Gemini), prompt templates for multi-file Flutter code.
    - **Agno Task Structure:** An Agno task taking PRD, returning code operations.
- **3.5. Integration Agent (`agent_system/integration_agent/`)**
    - **Purpose:** Apply generated code, manage dependencies, prepare and run the Flutter app for preview.
    - **Responsibilities:** Write/update files in project's isolated environment, update `pubspec.yaml`, run `flutter pub get`, run `flutter run -d web-server` (or similar), monitor for preview URL.
    - **Inputs:** Code operations from Generator Agent, `project_id`.
    - **Outputs:** Status (success/failure), logs from CLI commands, live preview URL.
    - **Tools:** File system ops, Flutter CLI (`subprocess` or Agno tool wrapper).
    - **Agno Task Structure:** An Agno task managing file ops and Flutter CLI calls. Long-running `flutter run` might require special handling by Agno or be managed as a separate background process by this agent.
- **3.6. Testing Agent (`agent_system/testing_agent/`)**
    - **Purpose:** Perform automated testing and analysis on the integrated, runnable application.
    - **Responsibilities:** Run `flutter analyze`, verify preview URL accessibility, (future) basic smoke tests, code quality/best practice audits, security checks. This runs *after* a preview link is available from the Integration Agent.
    - **Inputs:** Preview URL, path to integrated codebase, `project_id`.
    - **Outputs:** Test report/audit (analysis results, runtime status, identified issues).
    - **Tools:** Flutter CLI, HTTP client, (future) headless browser, LLM for code review.
    - **Agno Task Structure:** An Agno task executing tests.
- **3.7. Documentation Agent (`agent_system/documentation_agent/`)**
    - **Purpose:** Generate solution documentation tailored to the user's codebase and integration.
    - **Responsibilities:** Generate inline code comments, create a summary document (changes, SDK features, usage). "Complimentary agent for every other agent."
    - **Inputs:** Original query, PRD, final generated code, `project_id`, user codebase context.
    - **Outputs:** Updated code files with comments, solution summary document.
    - **Tools:** LLM for summarization and comment generation.
    - **Agno Task Structure:** An Agno task taking context and producing docs.
- **3.8. Settings Agent (Optional) (`agent_system/settings_agent/`)**
    - **Purpose:** Manage user/project-specific configurations.
    - **Responsibilities:** Store/retrieve preferences (code style, Flutter version) and provide them to other agents.
    - **Inputs:** User input for preferences.
    - **Outputs:** Configuration data.
    - **Tools:** Supabase client.
    - **Agno Task Structure:** Agno tasks for CRUD operations on settings.

**4. Data Flow & State Management**

- **Data Flow:** Artifacts like "Plan Document," "PRD," and code operations are passed between agents via the Orchestrator. The Orchestrator may store these temporarily or pass references to locations in Supabase Storage if they are large.
- **Agno Task Outputs:** Outputs from Agno tasks will be consumed by the Orchestrator. If Agno supports structured outputs, this will be straightforward. Otherwise, parsing from text/JSON may be needed.
- **Supabase State Tracking:** The `code_generations` table (or a new `agent_tasks` table) in Supabase will track the `task_id`, current processing agent, status (e.g., `RESEARCH_IN_PROGRESS`, `ANALYSIS_COMPLETE`, `GENERATION_FAILED`), and paths to key artifacts. Each agent updates this state via the Orchestrator or directly.
- **`asyncio.Queue` Bridge:** The `AgnoAgenticFlutterServiceImpl` uses a per-request `asyncio.Queue`. The Orchestrator (and by extension, the specialized agents) sends all streamable output (status updates, code chunks, logs, errors, final results) to this queue. The service then reads from this queue to call the `on_chunk` WebSocket callback.

**5. Asynchronous Processing & Performance**

- The Orchestrator will invoke Agno agent tasks asynchronously (`asyncio.create_task` if they are async Python functions managed within the same process, or via Agno's deployment/invocation mechanism if they are separate services/functions).
- For very long-running tasks (e.g., `flutter build`, complex RAG with multiple LLM calls), if Agno's native scaling/async isn't sufficient or ties up main process resources, consider dispatching these specific agent tasks to an external queue (Celery, RQ) as identified in the audit. The Agno task itself could be what's queued.
- Streaming from agents -> Orchestrator -> `asyncio.Queue` -> `AgnoAgenticFlutterServiceImpl` -> WebSocket ensures responsiveness.

**6. RAG Integration Details**

- **Research Agent:** May perform light RAG on an SDK overview or high-level user project structure.
- **Analysis Agent:** This is the primary RAG workhorse.
    - **Sources:** Detailed LikeMinds SDK docs (`docs.txt`, `code.txt`), ingested user project code (`ingest.txt` and specific files if needed).
    - **Pipeline:**
        1. Load relevant documents based on the "Plan Document."
        2. Implement code-aware chunking for Dart files, and text-aware chunking for Markdown.
        3. Generate embeddings (e.g., Gemini embeddings).
        4. Store/retrieve from a vector database (ChromaDB initially, then explore pgvector/others).
        5. Use hybrid search (semantic + keyword) for retrieval.
        6. Re-rank results using a cross-encoder or LLM for relevance.
        7. Pass top-k relevant, re-ranked chunks to an LLM (within the Analysis Agent) to synthesize the PRD.

**7. Error Handling & Resilience**

- **Agent-Level:** Each Agno agent task must have robust internal error handling. Errors should be caught and returned as structured output to the Orchestrator.
- **Orchestrator-Level:**
    - Receives error statuses from agents.
    - Decides on retries (with backoff for transient errors like API limits).
    - May invoke a different agent or a "fallback" strategy.
    - If unrecoverable, reports a detailed error to the `response_queue` for the user.
    - Ensures resource cleanup on failure (e.g., stopping runaway Flutter processes).

**8. Configuration**

- Existing `.env` variables for `GOOGLE_API_KEY`, `SUPABASE_URL`, etc.
- New variables for Agno if it has specific deployment or runtime configs.
- Potential configurations for individual agents (e.g., LLM model choice per agent, RAG retrieval parameters) can be managed via a `config.py` within `agent_system` or stored in Supabase (via Settings Agent).

**9. Testing Strategy for Agents**

- **Unit Tests:** Each Agno agent task/function should be unit-tested. Mock external dependencies (LLM calls, Flutter CLI, DB access).
- **Integration Tests:** Test sequences of agent calls via the Orchestrator for common scenarios (e.g., Research -> Analysis -> Generator). Mock only the outermost dependencies (e.g., actual LLM endpoint, but not the agent-to-agent calls).
- Focus on testing the PRD generation and code generation against that PRD.

**10. Deployment Considerations with Agno**

- Evaluate Agno's "built-in cloud deploy features." Can individual agents be deployed as scalable, independent functions/services?
- If so, the Orchestrator would invoke these deployed Agno apps (e.g., via HTTP requests).
- If not, the entire `agent_system` (including Agno-defined tasks) might run within the main FastAPI application's process(es), or be containerized together.
- Ensure environment variables and secrets are securely managed in the deployment environment for Agno apps.