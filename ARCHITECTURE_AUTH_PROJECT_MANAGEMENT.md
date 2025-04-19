# Authentication, User Management, Session Management, and Project Management: Implementation Plan

## Overview
This document outlines a detailed plan to add robust authentication, user management, session management, and project management to the LikeMinds Flutter Integration Assistant. The goal is to support multi-user, multi-project workflows with secure access, persistent sessions, and project isolation, while integrating seamlessly with the existing codebase and architecture.

---

## 1. **New Modules and Their Responsibilities**

### **1.1. Auth Module**
- Handles user registration, login, password reset, and token issuance (JWT).
- Provides decorators/middleware for protected endpoints.

### **1.2. User Management Module**
- CRUD operations for user profiles.
- Role and permission management (admin, user, guest).

### **1.3. Session Management Module**
- Tracks active sessions, supports session invalidation and refresh.
- Optionally supports persistent sessions (e.g., Redis-backed).

### **1.4. Project Management Module**
- CRUD for projects (each user can have multiple projects).
- Project sharing/collaboration (optional, for future expansion).
- Project-level settings and metadata.

---

## 2. **API Endpoints**

### **2.1. Auth Endpoints**
- `POST   /api/auth/register`         — Register a new user
- `POST   /api/auth/login`            — Login and receive JWT tokens
- `POST   /api/auth/logout`           — Invalidate current session
- `POST   /api/auth/refresh`          — Refresh access token
- `POST   /api/auth/reset-password`   — Request password reset
- `POST   /api/auth/change-password`  — Change password (authenticated)

### **2.2. User Endpoints**
- `GET    /api/users/me`              — Get current user profile
- `PUT    /api/users/me`              — Update own profile
- `GET    /api/users/{user_id}`       — (Admin) Get user by ID
- `GET    /api/users/`                — (Admin) List users
- `DELETE /api/users/{user_id}`       — (Admin) Delete user

### **2.3. Session Endpoints**
- `GET    /api/sessions/`             — List active sessions (self or admin)
- `DELETE /api/sessions/{session_id}` — Invalidate a session

### **2.4. Project Endpoints**
- `POST   /api/projects/`             — Create new project
- `GET    /api/projects/`             — List user's projects
- `GET    /api/projects/{project_id}` — Get project details
- `PUT    /api/projects/{project_id}` — Update project
- `DELETE /api/projects/{project_id}` — Delete project
- `POST   /api/projects/{project_id}/share` — (Future) Share project with another user

---

## 3. **Module Placement and Structure**

- `api/domain/auth/`           — Auth interfaces and models
- `api/infrastructure/auth/`   — Auth service implementations
- `api/presentation/auth.py`   — Auth API routes
- `api/domain/users/`          — User domain models
- `api/infrastructure/users/`  — User service implementations
- `api/presentation/users.py`  — User API routes
- `api/domain/sessions/`       — Session models
- `api/infrastructure/sessions/` — Session service
- `api/presentation/sessions.py` — Session API routes
- `api/domain/projects/`       — Project models
- `api/infrastructure/projects/` — Project service
- `api/presentation/projects.py` — Project API routes

---

## 4. **Integration with Existing Modules**

### **4.1. WebSocket & Code Generation**
- **Session Awareness:** WebSocket connections require authentication (JWT in query/header/cookie).
- **Project Context:** Each code generation or analysis request is tied to a project ID; only authorized users can access/modify a project.
- **User Context:** All actions are performed in the context of the authenticated user.

### **4.2. Existing API Enhancements**
- Add dependency injection for user/project context in all relevant endpoints.
- Restrict access to generated code, output, and integration flows by project ownership.
- Add audit logging for sensitive actions (project deletion, user management).

---

## 5. **Authentication & Session Flow**

1. **User registers or logs in** and receives JWT access and refresh tokens.
2. **Tokens are sent** with each API/WebSocket request (header/cookie).
3. **Session management** tracks active tokens and allows invalidation (logout, admin action).
4. **All project/code actions** are scoped to the authenticated user and selected project.

---

## 6. **Data Models (Sketch)**

### **User**
- id (UUID)
- email
- password_hash
- name
- roles (list)
- created_at, updated_at

### **Session**
- id (UUID)
- user_id
- created_at
- expires_at
- user_agent, ip_address

### **Project**
- id (UUID)
- owner_id (user)
- name
- description
- created_at, updated_at
- settings (JSON)

---

## 7. **Security Considerations**
- Passwords hashed with bcrypt/argon2.
- JWT tokens with short expiry, refresh tokens for session renewal.
- Rate limiting on auth endpoints.
- Email verification and password reset via email (optional, for future).

---

## 8. **Future Enhancements**
- **OAuth2/Social Login**
- **Multi-user project collaboration**
- **Role-based access control (RBAC)**
- **Audit logs and activity history**
- **Billing/subscription management**

---

## 9. **Migration/Refactor Plan for Existing Modules**
- Refactor WebSocket and code generation flows to require authentication and project context.
- Move any user/session logic from ad-hoc storage to the new modules.
- Update documentation and onboarding guides to reflect new flows.

---

## 10. **Example: Authenticated Code Generation Flow**
1. User logs in and selects a project.
2. User opens a WebSocket connection with JWT and project ID.
3. All code generation, analysis, and output is scoped to that project and user.
4. User can manage multiple projects, switch between them, and share if enabled.

---

## 11. **API Example: Project Creation**
```http
POST /api/projects/
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "name": "My First Integration",
  "description": "Integration for LikeMinds Chat SDK"
}
```

---

## 12. **Summary Table: New Endpoints**
| Area      | Endpoint                              | Method | Auth Required | Description                  |
|-----------|---------------------------------------|--------|---------------|------------------------------|
| Auth      | /api/auth/register                    | POST   | No            | Register new user            |
|           | /api/auth/login                       | POST   | No            | Login                        |
|           | /api/auth/logout                      | POST   | Yes           | Logout (invalidate session)   |
|           | /api/auth/refresh                     | POST   | No            | Refresh token                |
| User      | /api/users/me                         | GET    | Yes           | Get own profile              |
|           | /api/users/me                         | PUT    | Yes           | Update own profile           |
|           | /api/users/{user_id}                  | GET    | Admin         | Get user by ID               |
|           | /api/users/                           | GET    | Admin         | List users                   |
|           | /api/users/{user_id}                  | DELETE | Admin         | Delete user                  |
| Session   | /api/sessions/                        | GET    | Yes           | List active sessions         |
|           | /api/sessions/{session_id}            | DELETE | Yes           | Invalidate session           |
| Project   | /api/projects/                        | POST   | Yes           | Create project               |
|           | /api/projects/                        | GET    | Yes           | List projects                |
|           | /api/projects/{project_id}            | GET    | Yes           | Get project details          |
|           | /api/projects/{project_id}            | PUT    | Yes           | Update project               |
|           | /api/projects/{project_id}            | DELETE | Yes           | Delete project               |
|           | /api/projects/{project_id}/share      | POST   | Yes           | Share project (future)       |

---

## 13. **Conclusion**
This plan will enable secure, multi-user, multi-project workflows, laying the foundation for future collaboration, advanced permissions, and enterprise features. All new modules will follow the existing clean architecture, and existing modules will be refactored for seamless integration. 

---

## 14. **Implementation Status (As of [Current Date])**

### **14.1. Implemented Features**

*   **Core Setup:**
    *   Supabase credentials configured (`.env`).
    *   `SupabaseManager` implemented for DB interactions (`api/infrastructure/database.py`).
    *   Basic authentication helpers (`get_current_user`, `create_access_token`) added (`api/infrastructure/auth.py`).
*   **API Endpoints:**
    *   Auth: `/register`, `/login`, `/logout`.
    *   Users: `/users/me` (GET/PUT).
    *   Projects: `/projects/` (POST/GET), `/projects/{id}` (GET/PUT/DELETE), `/projects/{id}/share` (basic structure).
*   **Integration:**
    *   Routers for Auth, Users, Projects added to `main.py`.
    *   Authentication dependency (`get_current_user`) implemented and refined.
    *   WebSocket endpoint requires `token` and `project_id` parameters.
*   **Frontend Tester:**
    *   `integration_tester.html` updated for auth flow, token handling, project selection, and WebSocket connection.

### **14.2. Remaining Work & Critical Next Steps**

*   **Refresh Token Flow:** Implement the `/api/auth/refresh` endpoint and corresponding client-side logic to handle token expiration and renewal.
*   **Project Authorization:** Implement robust authorization checks within all project-related API endpoints and the WebSocket handler. Ensure users can only access/modify projects they own or are members of (using the `project_members` table). This is a **critical security item**.
*   **WebSocket Authorization:** Enhance `WebSocketHandler` to validate that the authenticated user has appropriate access rights to the specified `project_id` before allowing operations.
*   **Project Sharing:** Fully implement the `/api/projects/{project_id}/share` endpoint logic to manage the `project_members` table.
*   **Password Management:** Implement `/api/auth/reset-password` and `/api/auth/change-password` flows.
*   **(Optional) Admin Features:** Implement admin endpoints for user management if required.
*   **(Optional) Session Endpoints:** Decide if explicit session management endpoints are needed beyond Supabase token handling.
*   **Security:** Implement rate limiting and perform a thorough security review of all authorization logic.
*   **Testing:** Add comprehensive unit and integration tests.
*   **Documentation:** Update API documentation (e.g., OpenAPI spec). 