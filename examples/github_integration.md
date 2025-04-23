# GitHub Integration Guide

This guide explains how to integrate with GitHub using GitHub Apps in our application.

## OAuth vs GitHub App

Our application supports two methods for GitHub integration:

1. **GitHub OAuth** - For basic user authentication and access to public repositories (deprecated)
   - Used for user sign-in and authentication
   - Limited repository access based on user permissions
   - Simple to set up but limited in scope
   - **This method is now deprecated in favor of GitHub Apps**

2. **GitHub App** - For extended repository access with granular permissions
   - Installed on specific repositories or organizations
   - Provides more granular and specific permissions
   - Better for production use cases requiring repository access
   - Recommended approach for all integrations

## Setting Up the GitHub App

1. Create a GitHub App at: https://github.com/settings/apps/new
   - App name: YourAppName
   - Homepage URL: Your application URL
   - Callback URL: `{API_URL}/api/github/app/callback`
   - Webhook URL (optional): Your webhook endpoint if needed
   - Permissions:
     - Repository permissions:
       - Contents: Read & write
       - Metadata: Read-only
       - Pull requests: Read & write (if needed)
     - Organization permissions:
       - Members: Read-only (if needed)
   - Where can this GitHub App be installed? (Any account or specific organization)

2. After creating the app, note down:
   - App ID
   - Client ID
   - Client secret
   - Generate a private key and download it

3. Configure your environment variables:
   ```
   GITHUB_APP_ID=your-app-id
   GITHUB_APP_NAME=your-app-name
   GITHUB_APP_CLIENT_ID=your-client-id
   GITHUB_APP_CLIENT_SECRET=your-client-secret
   GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
   ```
   
   Note: For the private key, replace newlines with `\n` or use a multiline environment variable.

   **Alternatively, store private key in a .pem file (recommended):**
   ```
   GITHUB_APP_ID=your-app-id
   GITHUB_APP_NAME=your-app-name
   GITHUB_APP_CLIENT_ID=your-client-id
   GITHUB_APP_CLIENT_SECRET=your-client-secret
   GITHUB_APP_PRIVATE_KEY_PATH=/absolute/path/to/api/infrastructure/github/keys/github-app-private-key.pem
   ```
   
   The system looks for the private key in the following order:
   1. First tries to load from the file specified in `GITHUB_APP_PRIVATE_KEY_PATH`
   2. Falls back to the value in `GITHUB_APP_PRIVATE_KEY` if the file doesn't exist
   
   Private key files should be stored in `api/infrastructure/github/keys/` directory which is gitignored.

## Frontend Integration

### User Flow

1. **User Authentication**
   - User logs in to our application using their username/password or other auth method
   - User obtains an access token for API access

2. **GitHub App Installation**
   - User clicks "Install GitHub App" button in our application
   - Application redirects to GitHub App installation flow
   - User selects which repositories to install the app on
   - GitHub redirects back to our application with an installation ID

3. **Linking Installation to User**
   - Our application links the GitHub App installation to the user's account
   - Application generates installation tokens as needed to access GitHub

4. **Repository Access**
   - User can now list, select, and import repositories from GitHub
   - All GitHub operations use the installation tokens for authentication

## API Endpoints

### GitHub App Management

- `POST /api/github/app/install` - Get the URL to install the GitHub App
- `GET /api/github/app/callback` - Handle GitHub App installation callback
- `GET /api/github/app/installation` - Get the current user's GitHub App installation
- `POST /api/github/app/refresh-token` - Refresh the GitHub App token
- `DELETE /api/github/app/installation` - Unlink the GitHub App installation

### Repository Management

- `GET /api/github/repositories` - List the user's repositories
- `POST /api/github/repositories/import` - Import a repository
- `GET /api/github/repositories/{import_id}/status` - Get the status of a repository import

## Implementation Details

### GitHub App Authentication

The GitHub App authentication flow uses JWT for API authentication:

1. Generate a JWT signed with the app's private key
2. Use the JWT to obtain an installation token
3. Use the installation token for API requests

### Token Management

Installation tokens expire after 1 hour, so we need to refresh them:

1. Store the installation ID with the user record
2. When a token expires, generate a new JWT
3. Use the JWT to obtain a new installation token
4. Update the stored token

### Repository Operations

When a user wants to access a repository:

1. Check if we have a valid installation token
2. If not, generate a new one
3. Use the token to perform the requested operation

## Migration from OAuth to GitHub App

If you were previously using the OAuth flow, here's how to migrate:

1. Create and configure a GitHub App as described above
2. Update your environment variables with the GitHub App details
3. Direct users to the new GitHub App installation flow
4. On successful installation, the legacy OAuth token is replaced with the installation token

The legacy OAuth endpoints (`/api/auth/github` and `/api/auth/github/callback`) are still available but deprecated. 