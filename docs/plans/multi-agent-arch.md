**Overall Agentic Architecture for LikeMinds Flutter Integration Assistant (using Agno)**

The system will be composed of a central **Orchestrator Agent** that coordinates a team of specialized agents. Each specialized agent will be designed as a modular component, potentially an Agno app or a set of Agno-managed functions.

**1. Orchestrator Agent**

- **Purpose:** To manage the end-to-end workflow of a user's request, from initial query to final output (code, preview, documentation). It sequences tasks, passes data between agents, handles errors, and manages the overall state.
- **Key Responsibilities:**
    - Receive initial validated user requests (query, project context, auth details) from the FastAPI/WebSocket layer.
    - Determine the appropriate sequence of specialized agent invocations based on the request type (e.g., new generation, fix error, analyze existing project).
    - Manage the state of the overall task (e.g., `PENDING_REQUIREMENTS`, `ANALYZING`, `GENERATING_CODE`, `TESTING_FAILED`, `COMPLETED`).
    - Facilitate data flow between agents (e.g., passing the "Plan Document" from Research to Analysis, "PRD" from Analysis to Generator).
    - Implement retry logic or error handling strategies if an agent fails.
    - Coordinate the iterative loop for fixing errors (e.g., Testing Agent finds error -> Orchestrator routes back to Analysis/Generator).
    - Stream progress updates and final results back to the user via the WebSocket layer.
- **Inputs:** User query, project ID, user authentication context, ongoing task state.
- **Outputs:** Final integration result (preview link, code files, documentation), error messages, streamed progress updates.
- **Tools/Techniques (Agno Context):**
    - This will likely be a primary Python module defining the control flow logic.
    - It will invoke other agents, which are themselves Agno tasks/apps.
    - Uses Supabase for persistent state tracking of the overall job.
    - Might leverage an external task queue (Celery, RQ, Arq) if Agno's deployment model for individual agents isn't sufficient for long-running, decoupled processes.

**2. Research Agent**

- **User's Description:** An agent that breaks down our query into requirements in the user’s codebase and with respect to the SDK. Output → A simple doc describing the plan.
- **Formalized Purpose:** To understand the user's high-level request, identify core requirements, and produce an initial plan document outlining the scope and approach, considering both the target SDK and the user's existing project context (if applicable).
- **Key Responsibilities:**
    - Process the initial user query.
    - If an existing project is specified (e.g., GitHub repo):
        - Ensure the project code is available (e.g., triggers cloning/ingestion if not already done via the Orchestrator or a pre-step).
        - Perform a high-level scan/analysis of the user's codebase (`ingest.txt`) to understand its main structure, technologies, and potential integration areas relevant to the query.
    - Consult high-level SDK information (e.g., main features, purpose of different modules) to map the user's request to SDK capabilities.
    - Clarify ambiguities if possible (future: could involve asking the user clarifying questions if the Orchestrator supports this feedback loop).
    - Define the scope of the requested integration.
- **Inputs:** User query, `project_id`, access to user's codebase summary (e.g., `ingest.txt` if an existing project), high-level SDK overview.
- **Outputs:** A "Plan Document" (e.g., structured text or JSON) detailing:
    - Interpreted user goal.
    - Key SDK features involved.
    - Relevant areas in the user's codebase (if applicable).
    - High-level steps for the integration.
    - Potential challenges or considerations.
- **Tools/Techniques (Agno Context):**
    - LLM (Gemini) for natural language understanding and planning, guided by specific prompts.
    - Access to `gitingest` output or file system for user project context.
    - Basic RAG capabilities to query an overview of the LikeMinds SDK.
    - Could be an Agno app that takes the query and project context and returns the plan document.

**3. Analysis Agent**

- **User's Description:** From the output of the requirement agent, the document, this agent analyses the codebase, and our documentation, and code. To find points of integration, necessary configurations to run, extra code required. Output → Outputs a PRD for the generation agent to follow to the T.
- **Formalized Purpose:** To perform a deep technical analysis based on the "Plan Document" from the Research Agent. It dives into the specifics of the SDK documentation and the user's codebase to produce a detailed Product Requirements Document (PRD) for the Generator Agent.
- **Key Responsibilities:**
    - Take the "Plan Document" as a primary input.
    - Perform detailed RAG against the full LikeMinds SDK documentation (`docs.txt`, `code.txt`) to find precise API usage, class names, methods, parameters, and configuration steps relevant to the plan.
    - If an existing project, perform targeted analysis of the user's codebase (`ingest.txt` and potentially specific files) to identify exact integration points, existing patterns to follow, and necessary modifications.
    - Determine all necessary configurations (e.g., `pubspec.yaml` changes, initialization steps, permissions).
    - Identify any boilerplate or utility code that will be required but might not be directly part of the core SDK feature.
    - Define the structure of new files to be created and modifications to existing files.
- **Inputs:** "Plan Document" (from Research Agent), full SDK documentation, example SDK code, user's full codebase (if applicable), potentially project settings (from Settings Agent).
- **Outputs:** A detailed "Product Requirements Document (PRD)" (structured for machine and human readability, e.g., JSON or detailed Markdown) containing:
    - Specific files to be created/modified with paths.
    - Functions/classes to be implemented or updated.
    - Exact SDK APIs to be called with parameters.
    - Required dependencies and `pubspec.yaml` changes.
    - Configuration details.
    - Data models, state management considerations.
- **Tools/Techniques (Agno Context):**
    - Advanced RAG capabilities (semantic search, re-ranking) on SDK docs and user code.
    - LLM (Gemini) for synthesis and structuring the PRD.
    - Code parsing tools (e.g., AST analysis for Dart) could be beneficial for deeper code understanding.
    - An Agno app that orchestrates RAG and LLM calls to produce the PRD.

**4. Generator Agent**

- **User's Description:** This agent generates code as per the PRD inputted to it. It is based only around flutter for now. Also has access to the code, documentation, as a backup but goal should be to cover every step in PRD itself. Output → Multiple code files edited, generated, in the chosen directory.
- **Formalized Purpose:** To generate Flutter/Dart code based *strictly* on the detailed PRD provided by the Analysis Agent, ensuring multi-file output as required.
- **Key Responsibilities:**
    - Implement all specifications outlined in the PRD.
    - Generate code for new files.
    - Generate modifications for existing files (respecting the existing content and structure).
    - Adhere to Flutter and Dart best practices and the multi-file output format (e.g., `<file path="...">...</file>`).
    - Use the provided SDK documentation and example code as a reference or "backup" if the PRD has minor gaps, but the primary source of truth is the PRD.
- **Inputs:** "PRD" (from Analysis Agent), (backup/reference access to SDK documentation and code context).
- **Outputs:** A structured set of code operations:
    - List of new files to create with their full content.
    - List of existing files to modify with their complete new content.
    - Changes for `pubspec.yaml`.
- **Tools/Techniques (Agno Context):**
    - LLM (Gemini) specialized in code generation, heavily guided by the PRD through precise prompting.
    - Prompt templates designed for multi-file Flutter code generation.
    - An Agno app that takes the PRD and outputs the code operations.

**5. Integration Agent**

- **User's Description:** This agent takes care of all the shell and flutter commands that run the application for preview, and analyses for proper integration. Output → A preview link with the app running.
- **Formalized Purpose:** To take the generated/modified code files, integrate them into the project's file system, manage dependencies, and prepare/run the Flutter application for preview.
- **Key Responsibilities:**
    - Receive file operations (new/modified files) from the `Generator Agent`.
    - Write new files and update existing files in the project's isolated working directory (e.g., `output/<project_id>/integration/`).
    - Update `pubspec.yaml` with new dependencies.
    - Execute `flutter pub get` to ensure all dependencies are fetched.
    - (Optional, could be part of Testing Agent) Run `flutter analyze` *after* `pub get` to catch any integration-time static errors.
    - Execute `flutter run -d web-server --web-port <port>` (or similar) to build and start the web preview.
    - Monitor the output of the Flutter run command to confirm successful startup and capture the preview URL.
- **Inputs:** Code file operations (from Generator Agent), project ID, existing project structure.
- **Outputs:**
    - Status of integration (success/failure).
    - Logs from `flutter pub get` and `flutter run`.
    - A live preview URL if successful.
    - Errors if the build or run fails.
- **Tools/Techniques (Agno Context):**
    - File system operations.
    - Python `subprocess` module (or Agno's equivalent for tool execution) to call Flutter CLI commands.
    - Process management for the `flutter run` dev server.
    - Port management.
    - An Agno app that manages these command-line interactions and file operations.

**6. Testing Agent**

- **User's Description:** This agent tests everything, once a preview link is done. It will start out simple but will be able to handle more complex tasks too. Output → Audits about security, missed practices, anything that is a runtime issue.
- **Formalized Purpose:** To perform automated testing and analysis on the integrated and runnable Flutter application (after a preview link is available or the app is built).
- **Key Responsibilities:**
    - **Static Analysis (Pre-run or if run fails):** Execute `flutter analyze` (if not already fully covered by Integration Agent) and report findings.
    - **Runtime Checks (Post-preview):**
        - Verify the preview URL is accessible and returns a 200 OK.
        - (Future) Basic smoke tests: e.g., check if the main widget renders, if specific elements are present (could use headless browser or Flutter driver tests if feasible).
    - **Code Quality & Best Practices Audit:**
        - Analyze generated code for common Flutter anti-patterns or missed best practices (could use LLM with specific prompts or custom linters).
        - Basic security checks (e.g., hardcoded secrets, though this is less likely in generated UI code).
    - Report any runtime errors observed during basic interaction (if automated interaction is implemented).
- **Inputs:** Preview URL (from Integration Agent), path to the integrated codebase, project ID.
- **Outputs:** A test report/audit detailing:
    - `flutter analyze` results.
    - Runtime status (e.g., app is running at URL).
    - List of identified issues (security, best practices, runtime errors).
    - Overall pass/fail status.
- **Tools/Techniques (Agno Context):**
    - Flutter CLI (`flutter analyze`).
    - HTTP client to check preview URL.
    - (Future) Headless browser (e.g., Playwright, Selenium) or Flutter integration testing tools.
    - LLM (Gemini) for code review tasks.
    - An Agno app executing these tests.

**7. Documentation Agent**

- **User's Description:** This is a complimentary agent for every other agent. This will be able to produce custom docs given any context of the product. Starting with flutter chat, it will bee able to produce solution docs customised around the codebase of the user.
- **Formalized Purpose:** To generate relevant documentation for the implemented solution, tailored to the user's codebase and the specific integration performed.
- **Key Responsibilities:**
    - Can be invoked by the Orchestrator after a successful integration or on demand.
    - Generate inline code comments for the newly generated/modified code.
    - Create a summary document (`README_INTEGRATION.md` or similar within the project output) detailing:
        - The user's original requirement.
        - The implemented solution.
        - Files created/modified.
        - Key SDK features used.
        - How to run/use the integrated feature.
        - Customization points relevant to the user's codebase.
- **Inputs:** User's original query, the "PRD" (from Analysis Agent), the final generated code, `project_id`, user's codebase context.
- **Outputs:**
    - Updated code files with comments.
    - A solution summary/documentation file.
- **Tools/Techniques (Agno Context):**
    - LLM (Gemini) for natural language generation and code summarization.
    - Access to the generated code and project context.
    - An Agno app that takes the context and produces documentation artifacts.

**8. Settings Agent (Optional but Recommended)**

- **Formalized Purpose:** To manage and provide configuration settings that influence the behavior of other agents, allowing for user preferences and project-specific adjustments.
- **Key Responsibilities:**
    - Store and retrieve user preferences (e.g., preferred code style, verbosity of documentation, default Flutter version if a choice).
    - Store and retrieve project-specific settings (e.g., if the project uses a specific state management library, linting rules, target platforms for preview).
    - Provide these settings to other agents as needed (e.g., `Generator Agent` might adjust code style, `Analysis Agent` might consider specific linter rules).
- **Inputs:** User input for preferences, project-specific configurations.
- **Outputs:** Configuration data consumable by other agents.
- **Tools/Techniques (Agno Context):**
    - Likely interacts with Supabase to store user/project settings.
    - Could be a simple Agno app/service providing a configuration API.

---

This formalized plan provides a more detailed blueprint for each agent. The success of this architecture will depend on:

- **Well-defined APIs/interfaces** between the Orchestrator and each specialized agent.
- **Robust error handling and state tracking** by the Orchestrator.
- The ability of Agno to efficiently run these (potentially numerous and sometimes long-running) agent tasks, either through its native deployment model or by integrating smoothly with external task queues.
- Clear and effective prompts for all LLM-driven agents.

This structure is well-suited for building a sophisticated, maintainable, and extensible AI assistant.