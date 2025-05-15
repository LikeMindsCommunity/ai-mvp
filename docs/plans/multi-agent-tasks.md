**Task & Story Breakdown for Engineer**

This breakdown assumes an agile approach with Epics, User Stories, and Tasks. Tasks are relatively sized (S, M, L, XL) for initial planning.

**Phase 0: Setup & Familiarization**

- **Epic: Agno Framework Integration Foundation**
    - **Story: Engineer can set up and run basic Agno applications.**
        - Task (M): Install Agno, review `docs.agno.com`, complete tutorials.
        - Task (S): Create a "Hello World" Agno app/task that calls the Gemini API.
        - Task (M): Experiment with Agno's deployment features (if any) for the "Hello World" app.
        - Task (S): Configure Agno to use existing project secrets/env variables.
    - **Story: Project structure for the new `agent_system` is established.**
        - Task (S): Create the `agent_system/` top-level directory and sub-directories for Orchestrator and initial agents (Research, Analysis, Generator).
        - Task (S): Define basic `__init__.py` and placeholder files for agent modules.

**Phase 1: Core Service Bridge & Orchestrator Skeleton**

- **Epic: Establish API to Agent System Communication**
    - **Story: `WebSocketHandler` can delegate requests to the new agent system via a service facade.**
        - Task (M): Create `AgnoAgenticFlutterServiceImpl` implementing `FlutterGeneratorService`.
        - Task (L): Implement the `asyncio.Queue`per-request mechanism within `_execute_agentic_flow` in the new service to handle the `on_chunk` callback.
        - Task (S): Modify `WebSocketHandler` to instantiate and use `AgnoAgenticFlutterServiceImpl`.
    - **Story: A basic Orchestrator Agent can receive tasks and manage a simple state.**
        - Task (M): Implement `agent_system.OrchestratorAgent` with a main `process_request(payload)` method.
        - Task (S): The `process_request` method should accept the `response_queue` from the payload.
        - Task (M): Implement initial state tracking for a task in Supabase's `code_generations` table (e.g., `status = 'ORCHESTRATOR_RECEIVED'`).
        - Task (S): Orchestrator should send a basic acknowledgment message to the `response_queue`.

**Phase 2: Implementing Core Agents (Research, Analysis, Generator)**

- **Epic: Develop Initial Agent Capabilities for Code Planning and Generation**
    - **Story: Research Agent can understand user query and produce a Plan Document.**
        - Task (M): Define the Agno task structure for the Research Agent.
        - Task (L): Implement LLM prompting for query understanding and high-level planning (consider user codebase summary and SDK overview).
        - Task (S): Define the schema/structure for the "Plan Document" output.
        - Task (M): Integrate Research Agent into the Orchestrator sequence.
    - **Story: Analysis Agent can consume Plan Document and produce a detailed PRD using RAG.**
        - Task (M): Define the Agno task structure for the Analysis Agent.
        - Task (XL): Implement RAG pipeline:
            - Task (M): Document loading for SDK docs (`docs.txt`, `code.txt`) and user code (`ingest.txt`).
            - Task (M): Code-aware and text-aware chunking strategies.
            - Task (S): Embedding generation (Gemini embeddings).
            - Task (M): Vector store interaction (ChromaDB initially).
            - Task (L): Retrieval (semantic search, filtering by plan) and re-ranking.
        - Task (L): Implement LLM prompting to synthesize the PRD from the Plan Document and RAG results.
        - Task (M): Define the schema/structure for the "PRD" output.
        - Task (M): Integrate Analysis Agent into the Orchestrator sequence.
    - **Story: Generator Agent can generate multi-file Flutter code based on a PRD.**
        - Task (M): Define the Agno task structure for the Generator Agent.
        - Task (L): Implement LLM prompting for multi-file code generation, strictly following the PRD.
        - Task (M): Implement parsing of the multi-file format (`<file path="...">`) from LLM output.
        - Task (S): Handle backup access to docs/code if PRD is insufficient (error handling).
        - Task (M): Integrate Generator Agent into the Orchestrator sequence.

**Phase 3: Implementing Execution Agents (Integration, Testing)**

- **Epic: Enable Code Integration, Preview, and Basic Testing**
    - **Story: Integration Agent can set up project files and dependencies, and run the app for preview.**
        - Task (M): Define Agno task structure for Integration Agent.
        - Task (M): Implement logic to save/update multiple files from Generator Agent output into the isolated project environment.
        - Task (S): Implement `pubspec.yaml` modification.
        - Task (M): Implement `flutter pub get` execution (via `subprocess` or Agno tool).
        - Task (L): Implement `flutter run -d web-server` execution, including process management, log streaming (to Orchestrator/response_queue), and preview URL capture. This task may need careful handling of long-running processes within Agno's model or offloading.
        - Task (M): Integrate Integration Agent into the Orchestrator sequence.
    - **Story: Testing Agent can perform static analysis and basic runtime checks.**
        - Task (M): Define Agno task structure for Testing Agent.
        - Task (M): Implement `flutter analyze` execution and output parsing.
        - Task (S): Implement HTTP check for preview URL accessibility.
        - Task (S): Define structure for the "Test Report/Audit" output.
        - Task (M): Integrate Testing Agent into the Orchestrator sequence, especially for the error-fixing loop.

**Phase 4: Rounding out Functionality (Documentation, Settings, Iteration)**

- **Epic: Enhance User Experience and System Adaptability**
    - **Story: Documentation Agent can generate code comments and solution summaries.**
        - Task (M): Define Agno task structure for Documentation Agent.
        - Task (L): Implement LLM prompting for generating inline comments based on generated code.
        - Task (L): Implement LLM prompting for generating a summary document (changes, SDK features, usage).
        - Task (S): Integrate Documentation Agent into the Orchestrator (e.g., after successful testing).
    - **Story (Optional): Settings Agent can manage user/project configurations.**
        - Task (M): Define Agno task(s) for Settings Agent (CRUD for settings).
        - Task (M): Integrate with Supabase to store settings.
        - Task (S): Modify other agents (e.g., Generator, Analysis) to optionally consume settings.
    - **Story: Orchestrator can handle the iterative error-fixing loop.**
        - Task (L): Implement logic in Orchestrator to take error feedback from Testing Agent, re-invoke Analysis/Generator agents with context about the error, and limit retry attempts.

**Phase 5: Robustness, Performance, and Final Integration**

- **Epic: Production Hardening and Optimization**
    - **Story: The agent system is robust with proper error handling.**
        - Task (L): Implement comprehensive error handling and structured error reporting in each agent and the Orchestrator.
        - Task (M): Implement retry mechanisms for transient errors (e.g., LLM API rate limits) in the Orchestrator or relevant agents.
    - **Story: The agent system is performant and handles long-running tasks efficiently.**
        - Task (L): If Agno's native execution model isn't sufficient for long-running tasks like `flutter run` or complex analysis chains, integrate an external task queue (Celery/RQ/Arq). The Orchestrator would dispatch jobs, and workers would execute Agno agent tasks.
        - Task (M): Optimize RAG pipeline (batching, efficient querying, caching if applicable).
        - Task (M): Optimize LLM interactions (prompt tuning, reducing token usage).
    - **Story: All functionalities from the old `flutter_generator` are covered by the new agent system.**
        - Task (M): Conduct a gap analysis and ensure feature parity.
        - Task (S): Refactor any remaining direct usages of `flutter_generator` components in the `api` layer to use the new service facade.
    - **Story: The old `flutter_generator` module is safely deprecated and removed.**
        - Task (S): Mark `flutter_generator` as deprecated.
        - Task (S): After successful testing and a soak period, remove the `flutter_generator` directory.

**Phase 6: Testing & Documentation (Ongoing throughout all phases)**

- **Epic: Ensure Quality and Maintainability**
    - **Story: Each agent has comprehensive unit tests.**
        - Task (Ongoing M-L per agent): Write unit tests for each Agno agent, mocking external dependencies (LLMs, CLI tools, DB).
    - **Story: Key agent interaction flows are covered by integration tests.**
        - Task (Ongoing L-XL): Write integration tests for common sequences managed by the Orchestrator (e.g., full code generation flow).
    - **Story: The system is documented for developers and future maintenance.**
        - Task (S): Update this ED as development progresses.
        - Task (M): Add code-level documentation (docstrings) for all new modules and classes.
        - Task (S): Document any new environment variables or configurations.

This breakdown provides a detailed roadmap. The engineer should start with Phase 0 and 1 to establish the core communication bridge and understand Agno, then iteratively build out the specialized agents and their integration into the Orchestrator. Each story can be further broken down into smaller, manageable technical tasks. Remember to allow for flexibility as the understanding of Agno's capabilities and limitations deepens.