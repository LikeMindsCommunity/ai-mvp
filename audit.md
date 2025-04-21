# Audit
Below is a consolidated technical audit that cross‑checks the actual source tree against the architecture described in `ed.md`.  I focus on the “critical path” that lets a request travel from an authenticated REST‑/WebSocket client through the FastAPI backend, into `FlutterGeneratorServiceImpl`, and back to the client, while persisting metadata in Supabase.

────────────────────────────────────────────────────────
1.  Auth Flow & JWT handling
────────────────────────────────────────────────────────
✓  Good
• `api/presentation/auth.py` offers register / login / logout endpoints.
• `api/infrastructure/auth/service.py` wraps Supabase Auth provider calls.
• `api/infrastructure/auth/jwt.py::get_current_user` simply proxies the token to
  `supabase.client.auth.get_user`, which is the recommended pattern.

⚠  Gaps / Risks
• Token refresh is missing.  Supabase access tokens expire after 1 hr; the
  client will suddenly start receiving `401` from websocket and REST calls.
  ⇒ Provide `/api/auth/refresh` that calls
     `client.auth.refresh_session({'refresh_token': …})`
  and update the websocket handshake to accept refresh tokens OR reconnect.

• Logout endpoint clears ONLY the client‑side session on *this* backend
  instance:  
  ```py
  client.auth.sign_out()        # ← doesn’t revoke JWT on Supabase side
  ```
  ⇒ Call Supabase Admin auth endpoint (or the up‑coming Management API) to
     revoke the actual refresh token, or document that “logout means best‑effort”.

• `OAuth2PasswordBearer` is declared with
  ```
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
  ```
  but the token issuing route is `/api/auth/login/oauth`.  
  ⇒ Fix path or add an alias; otherwise Swagger UI “Authorize” won’t work.

────────────────────────────────────────────────────────
2.  Project isolation & RLS
────────────────────────────────────────────────────────
✓  Good
• Every POST/PUT/DELETE in `api/infrastructure/projects/service.py` explicitly
  sets `client.postgrest.auth(jwt)` which is necessary for Supabase RLS.

⚠  Gaps / Risks
• No explicit database RLS policies included in the repo.  Without them, reading
  arbitrary project rows is possible by simply using an owner’s JWT.  
  ⇒ Add SQL migrations with policies:
     ```
     create policy "project_select_for_member"
       on projects for select
       using (   owner_id = auth.uid()
              or id in (select project_id
                        from project_members
                        where user_id = auth.uid()) );
     ```

• Missing migration management: there is no `migrations/` folder or any call to
  Supabase CLI.  You will lose schema drift awareness.  
  ⇒ Adopt `supabase/migrations` + CI check.

────────────────────────────────────────────────────────
3.  Code‑generation lifecycle
────────────────────────────────────────────────────────
Sequence (ideal):
  1）WebSocket `/api/flutter` → `WebSocketHandler`
  2）`get_current_user` validates token
  3）`service.get_project` ensures membership
  4）`FlutterGeneratorServiceImpl` handles code

✓  Good
• `WebSocketHandler` creates a `code_generations` row before every run and
  updates it afterwards – good auditable trail.

• Conversation history is kept per `session_id` using in‑memory dict.  Keeps
  prompts contextual.

⚠  Gaps / Risks
• In‑memory conversation state means *every Uvicorn worker* has its own copy.
  On a multi‑process deploy (Gunicorn + Uvicorn workers, or Kubernetes pods)
  conversation context will be lost.  
  ⇒ Persist history in Supabase or Redis keyed by `(project_id, session_id)`.

• `FlutterGeneratorServiceImpl.generate_flutter_code` performs long‑running
  CPU / I/O tasks (Gemini streaming, `flutter pub get`, running a PTY web‑server)
  inside the FastAPI worker thread.  
  – Blocks the event‑loop, starves other requests.  
  – PTY stays open even if client disconnects.  
  ⇒ Off‑load heavy tasks to a background queue (Celery/RQ/Arq) and stream
     status via PubSub / `sse-starlette`.

• No cancellation / cleanup when websocket closes:
  `except WebSocketDisconnect: pass` simply ignores; but the Flutter hot‑reload
  server is still running in a thread.  
  ⇒  On disconnect call `integration_manager.stop_flutter_app()` and clean tmp
      directories.

• `integration/` project is shared by *all* users; concurrent writes to
  `integration/lib/main.dart` will race.  
  ⇒  Copy a template into `output/<project_id>/<generation_id>/integration/`
      per generation OR use git worktrees.

• `run_command_with_timeout` captures entire output in memory then joins.
  For `flutter pub get` the output can exceed dozens of MB → memory bloat.
  ⇒  Stream chunks to the websocket as they arrive, keep a rolling buffer for
     tail lines only.

────────────────────────────────────────────────────────
4.  Supabase schema write‑paths
────────────────────────────────────────────────────────
• `code_generations.status` is set to `"pending"`; later update uses
  `"completed"` or `"error"` but RLS policies not shown.
  ⇒  Need `alter type` or `check (status in …)` and RLS allowing only owner.

• No indices on `code_generations.project_id` or `user_id`.  Large tables will
  slow SELECTs from PostgREST.

────────────────────────────────────────────────────────
5.  Configuration / Secrets
────────────────────────────────────────────────────────
⚠
• Google API key, Supabase service key pulled straight from environment – good –  
  but `.env.example` is missing so newcomers won’t know required vars.

• `Settings` stores `jwt_secret` although all auth is forwarded to Supabase;
  consider removing to avoid confusion.

────────────────────────────────────────────────────────
6.  Error handling & client contract
────────────────────────────────────────────────────────
• `WebSocketHandler.on_chunk` throttles only `Text`/`Chat`, but a big `Code`
  block can exceed browser’s frame size; consider slicing code too.

• JSON schema for outbound websocket events not formally defined. Generators
  may emit unexpected keys.  Recommend a `pydantic.BaseModel` (with `model_dump`).

────────────────────────────────────────────────────────
7.  Missing Observability & Ops
────────────────────────────────────────────────────────
• No structured logging (just `print`).  Replace with `loguru` or stdlib logger
  and attach request_id / project_id.

• No health‑check for flutter hot‑reload thread aside from basic HTTP ping.  
  If Dart process crashes, the thread flag `is_running` remains False but
  nothing restarts it.

• CI pipeline absent (lint, tests, Supabase diff).

────────────────────────────────────────────────────────
8.  Suggested Immediate Road‑map
────────────────────────────────────────────────────────
1.  Data‑layer
    • Add SQL migrations (`supabase db diff` → commit) for projects,
      code_generations, RLS policies, indices.
    • Introduce Alembic if local Postgres, else rely on Supabase CLI.

2.  Task execution
    • Introduce a background worker (Celery + Redis) with a `queue_id`
      stored in `code_generations`.
    • WebSocket only streams database polling results; if client disconnects
      worker still finishes and marks row.

3.  Conversation persistence
    • New table `conversation_history` (`project_id`, `session_id`, `messages`)
      OR Redis HASH with TTL.
4.  Proper token refresh endpoint and integration in WebSocket handshake.

5.  Multi‑tenant `integration/`
    • Use per‑generation temp directories; optionally reuse Docker image for
      Flutter SDK to guarantee reproducibility.

6.  Observability
    • Adopt `structlog` + OpenTelemetry traces.
    • Add Prometheus metrics: code_generation_duration_seconds,
      flutter_analyze_fail_total.

7.  Unit & e2e tests
    • Mock Gemini client and Flutter CLI to test generation pipeline quickly.
    • Add `pytest‑asyncio` tests for WebSocket route.

────────────────────────────────────────────────────────
Bottom line
────────────────────────────────────────────────────────
The project already follows the layered architecture described in `ed.md`; the
biggest technical debts are around long‑running tasks inside the FastAPI event
loop, missing RLS/migrations, lack of token refresh, and race‑conditions on the
shared `integration/` project.  Addressing the **task‑off‑loading**, **RLS
policies**, and **per‑generation isolation** will provide the biggest reliability
wins for production readiness.
