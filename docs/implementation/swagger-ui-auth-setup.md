# Swagger UI Authentication Setup

This document describes how to implement and test the authentication flow for Swagger UI in our application.

## Current Implementation

We've already updated the OAuth2PasswordBearer configuration in `api/infrastructure/auth/jwt.py` to point to the correct endpoint:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/oauth")
```

This configuration tells Swagger UI which endpoint to use for authentication. The specified endpoint (`/api/auth/login/oauth`) is designed to accept username and password in the format expected by the OAuth2 Password flow.

## Adding an Alias Route (Optional)

In some cases, it may be helpful to add an alias route to simplify the authentication flow. Here's how to implement it:

1. Open the auth router file (`api/presentation/auth.py`)
2. Add a new route that aliases to the existing OAuth endpoint:

```python
# This is the original OAuth endpoint
@router.post("/login/oauth")
async def login_with_oauth_form(form_data: OAuth2PasswordRequestForm = Depends()):
    # Existing implementation...
    pass

# Add this alias for Swagger UI - it will redirect to the OAuth endpoint
@router.post("/swagger-auth")
async def swagger_auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Alias endpoint for Swagger UI authentication.
    This is an alias for /api/auth/login/oauth that may be easier to find.
    """
    return await login_with_oauth_form(form_data)
```

3. Update the OAuth2PasswordBearer configuration to use this new endpoint:

```python
# In api/infrastructure/auth/jwt.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/swagger-auth")
```

## Testing the Authentication Flow

To test the Swagger UI authentication:

1. Navigate to the Swagger UI documentation page (typically at `/docs`)
2. Click the "Authorize" button at the top right
3. Enter valid user credentials:
   - Username: User's email address
   - Password: User's password
4. Click "Authorize"
5. If successful, the Swagger UI will now include the authorization token with all requests

## Troubleshooting

If Swagger UI authentication is not working:

1. **Check Network Requests**: Use browser developer tools to inspect the network request made when clicking "Authorize"
2. **Verify Endpoint Existence**: Ensure the endpoint specified in `tokenUrl` exists and is accessible
3. **Test Direct API Call**: Try calling the authentication endpoint directly using a tool like Postman
4. **Review Error Messages**: Check for specific error messages in the response
5. **CORS Issues**: Make sure CORS is properly configured to allow requests from the Swagger UI origin

## Notes on Implementation

- The OAuth2PasswordBearer in FastAPI expects a specific response format from the authentication endpoint
- The endpoint must return a JSON object with at least `access_token` and `token_type` fields
- The original `/api/auth/login/oauth` endpoint is specifically designed to meet these requirements
- Any alias endpoint must return the exact same format 