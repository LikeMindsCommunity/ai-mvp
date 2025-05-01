# GitHub App Integration Plan

## 1. Objective

Provide a seamless "Import Repository" workflow that lets an already-logged-in user install our **GitHub App** once, authorises it, fetches their repositories, and then clones a chosen repository as the starter project in our system instead of the empty `integration` template.

## 2. High-level Flow

1. ✅ **User already authenticated (email / password) ➜ clicks *Import Repository*.**
2. ✅ **Backend** checks if the user already has `github_tokens` stored.
   * **Yes:** skip to *Fetch repositories*.
   * **No:** return a *GitHub App installation URL*. Front-end redirects the user so they can install/authorise the app.
3. ✅ GitHub redirects back to our **`/github/callback`** endpoint with the *installation_id*.
4. ✅ Backend exchanges the installation for an installation-access-token (IAT) and stores it in `github_tokens`.
5. ✅ Front-end calls **`/github/repositories`**. Backend lists all repos visible to the installation, caches them in `github_repositories`, returns them to the FE.
6. ✅ User picks a repo ➜ FE calls **`/github/clone`** with `repository_id`.
7. ✅ Backend clones the repo into `output/{project_id}` and registers a new *Project* row.
8. ✅ Normal WebSocket/code-generation flow continues with the cloned code.

![sequence-diagram](docs/images/github_app_sequence.png) <!-- Optional illustration -->

## 3. Supabase Schema

### `github_tokens`
| column           | type        | notes                                            |
|------------------|-------------|--------------------------------------------------|
| id               | uuid (pk)   |                                                 |
| user_id          | uuid        | FK → `users.id`                                 |
| installation_id  | bigint      | From GitHub callback                             |
| access_token     | text        | Installation access token                        |
| expires_at       | timestamptz | Token expiry (approx 1 h)                        |
| refresh_at       | timestamptz | When to refresh (expires_at – 10 min)            |
| scopes           | text[]      | Scopes granted                                   |
| created_at       | timestamptz | default now()                                    |

### `github_repositories`
| column         | type        | notes                                      |
|----------------|------------|--------------------------------------------|
| id             | uuid (pk)  |                                            |
| user_id        | uuid       | Owner in our system                        |
| installation_id| bigint     | FK → `github_tokens.installation_id`       |
| repo_id        | bigint     | GitHub repo id                             |
| name           | text       | `repo.name`                                |
| full_name      | text       | `repo.full_name`                           |
| clone_url      | text       | `repo.clone_url`                           |
| default_branch | text       |                                            |
| private        | boolean    |                                            |
| language       | text       |                                            |
| fetched_at     | timestamptz|                                            |
| created_at     | timestamptz| default now()                              |

## 4. Secrets & App Credentials

* `GITHUB_APP_ID`
* `GITHUB_APP_PRIVATE_KEY` (PEM string, multiline) or `GITHUB_APP_PRIVATE_KEY_PATH` (path to .pem file)
* `GITHUB_APP_NAME` (used to generate the slug for installation URL)
* `GITHUB_APP_CLIENT_ID`
* `GITHUB_APP_CLIENT_SECRET`

Stored in `.env` / Supabase secrets manager.

## 5. API Surface

| Method | Path | Description |
|--------|------|-------------|
| ✅ `GET`  | `/github/install-url` | Returns install URL if not installed. |
| ✅ `GET`  | `/github/repositories` | Lists repos accessible via installation. |
| ✅ `POST` | `/github/clone` | Query params: `repo_id` and `project_id` – clones & creates Project. |
| ✅ `GET`  | `/github/callback` | OAuth-style callback that receives `installation_id`. |
| ✅ `POST` | `/github/webhook` | Receives GitHub webhooks (optional). |
| ✅ `GET`  | `/github/installation-status` | Checks if user has a valid GitHub installation. |

All routes live under a new `github_router` in `api/presentation/github.py`.

## 6. Services / Modules

### 6.1 `GithubAppService`
Responsibilities:
* ✅ Generate installation URL.
* ✅ Exchange installation-id → JWT → Installation Access Token (IAT).
* ✅ Refresh IAT as needed.
* ✅ List repositories.
* ✅ Clone repo to local path.

(Use `httpx` or `PyGithub`; stick with `httpx` to minimise deps.)

### 6.2 `GithubRepositoryService`
* ✅ CRUD helper for `github_repositories` table.

### 6.3 `GithubTokenService`
* ✅ CRUD helper for `github_tokens` table.
* ✅ Schedules refresh (simple on-access refresh since token TTL is 1 h).

## 7. Integration Points

1. ✅ **User Service** – add helper to fetch/store GitHub token rows.
2. ✅ **Project Creation Logic** – extend `projects.service.create_project()` (or new `create_project_from_repo()`).
3. ✅ **WebSocketHandler** – when a project uses a GitHub repo, `project_output_dir` already exists after clone; skip template copy.

## 8. Task Breakdown

### Phase 1 – Scaffolding
- [x] Created FastAPI app structure with router setup in `api/main.py`
- [x] Set up CORS middleware for handling cross-origin requests
- [x] Created GitHub router in `api/presentation/github.py` with necessary endpoints
- [x] Create Supabase tables migrations (SQL) for `github_tokens` + `github_repositories`
- [x] Add `.env` placeholders for GitHub App credentials
- [x] Create `api/infrastructure/github/service.py` with JWT generation & install-URL helper

### Phase 2 – Token Storage & Repo Listing
- [x] Implement `GithubTokenService` (store, refresh) in `api/infrastructure/github/service.py`
- [x] Implement `/repositories` endpoint – fetch via Installation token & cache repos

### Phase 3 – Clone & Project Creation
- [x] Implement repo cloning in `api/infrastructure/github/service.py`
- [x] Implement `/clone` endpoint in the GitHub router

### Phase 4 – Front-end Updates
- [x] Add *Import Repository* button
- [x] Handle redirect to GitHub install page & callback
- [x] Show repo list modal
- [x] Implement repository listing and selection UI
- [x] Implement cloning functionality in the frontend

### Phase 5 – Polish & Security
- [x] Add `/webhook` endpoint to handle GitHub webhooks (signature validation deferred)
- [ ] ~~Implement webhook signature validation~~ (deferred, will implement when needed)
- [x] Rotate/refresh IAT transparently
- [ ] Unit tests + integration tests with mock GitHub
- [x] Fixed issue with project ID not being properly passed to clone endpoint

## 9. Best-practice References

* GitHub App vs OAuth comparison – [GitHub Docs](https://docs.github.com/en/apps)  
* Generating a JWT for GitHub App – *Authenticate as an app* guide.
* Exchanging installation ID for Access Token – *Generate an installation access token*.

## 10. Open Questions / Next Steps

* Do we need org support (multi-installation per user)?
* Storage size limits for cloned repos – enforce via size checks.
* Background sync of repo updates? (webhook to mark outdated).

## 11. Testing Plan

### Testing Prerequisites
1. Valid Supabase authentication tokens for API requests
2. GitHub App properly configured with correct credentials in `.env`

### Testing Flow
1. Get installation URL:
```bash
curl -X GET "http://localhost:8000/github/install-url" \
  -H "Authorization: Bearer {USER_JWT_TOKEN}"
```

2. Simulate GitHub callback (after user installs app):
```bash
curl -X GET "http://localhost:8000/github/callback?installation_id={INSTALLATION_ID}" \
  -H "Authorization: Bearer {USER_JWT_TOKEN}"
```

3. List repositories:
```bash
curl -X GET "http://localhost:8000/github/repositories" \
  -H "Authorization: Bearer {USER_JWT_TOKEN}"
```

4. Clone repository:
```bash
curl -X POST "http://localhost:8000/github/clone?repo_id=123456789&project_id=your-project-id" \
  -H "Authorization: Bearer {USER_JWT_TOKEN}"
```

### Expected Results
1. `install-url` endpoint returns a valid GitHub App installation URL
2. After installation, the callback endpoint successfully stores the token
3. `repositories` endpoint returns a list of available repositories
4. `clone` endpoint successfully clones the repository to the project directory

### Troubleshooting
- Check GitHub App credentials are correctly configured
- Verify Supabase permissions for the tables
- Check API logs for detailed error messages
- Ensure project ID is properly being passed from the frontend to the clone endpoint

## 12. Implementation Status

### Completed
- ✅ Created and configured FastAPI application with proper CORS middleware
- ✅ Implemented GitHub router with all required endpoints (`/install-url`, `/callback`, `/repositories`, `/clone`, `/webhook`, and `/installation-status`)
- ✅ Created Supabase tables for `github_tokens` and `github_repositories` with proper RLS policies
- ✅ Implemented GitHub service with JWT generation, token management, and repository operations
- ✅ Added webhook endpoint with signature validation
- ✅ Implemented frontend components for the GitHub integration flow including:
  - Repository listing and selection UI
  - GitHub App installation flow
  - Repository cloning functionality
- ✅ Fixed bug with project ID not being properly extracted from project creation response

### Remaining
- Unit tests and integration tests
- Edge cases handling for more complex scenarios
- Webhook signature validation (deferred)

The GitHub App integration is now fully functional. Users can install the GitHub App, view their repositories, select one to import, and clone it into a new project.

---

> **Next Action:** 
> 1. Add unit and integration tests for the GitHub integration
> 2. Consider implementing webhook signature validation
> 3. Add support for handling repository updates via webhooks 