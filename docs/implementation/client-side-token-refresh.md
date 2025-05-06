# Client-Side Token Refresh Implementation

This document provides implementation details for handling refresh tokens on the client side.

## Secure Storage of Refresh Tokens

### Browser-Based Applications

For browser-based applications, secure cookies are recommended for storing refresh tokens.

```javascript
// Set secure cookies on login success
function storeAuthTokens(accessToken, refreshToken) {
  // Set HttpOnly cookie for refresh token (should be set by server)
  // Client can't directly set HttpOnly cookies, so this would be a server-side operation
  
  // For development/example purposes, we can use regular cookies
  document.cookie = `refresh_token=${refreshToken}; path=/; SameSite=Lax; Secure`;
  
  // Store access token in memory (preferred) or sessionStorage for immediate use
  sessionStorage.setItem('access_token', accessToken);
}
```

### Mobile Applications

For mobile applications, use platform-specific secure storage solutions:

```javascript
// React Native example using react-native-keychain
import * as Keychain from 'react-native-keychain';

async function storeAuthTokens(accessToken, refreshToken) {
  // Store refresh token in secure keychain
  await Keychain.setGenericPassword(
    'refresh_token',
    refreshToken,
    {
      service: 'auth',
      accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY,
      accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED
    }
  );
  
  // Store access token in memory for immediate use
  // Optionally store in secure storage as well
  await Keychain.setGenericPassword(
    'access_token',
    accessToken,
    {
      service: 'auth_token',
      accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED
    }
  );
}
```

## Token Refresh Logic

Implement token refresh logic to handle token expiration before making API calls:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'YOUR_SUPABASE_URL';
const supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY';
const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function getRefreshToken() {
  // For browser apps, retrieve from cookies (if not HttpOnly)
  const cookies = document.cookie.split(';');
  const refreshTokenCookie = cookies.find(cookie => cookie.trim().startsWith('refresh_token='));
  if (refreshTokenCookie) {
    return refreshTokenCookie.split('=')[1];
  }
  
  // For mobile apps, retrieve from secure storage
  // const credentials = await Keychain.getGenericPassword({ service: 'auth' });
  // return credentials.password;
  
  return null;
}

// Function to check if token is expired or will expire soon
function isTokenExpiring(token) {
  if (!token) return true;
  
  try {
    // Decode JWT to get expiration time
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
    
    const { exp } = JSON.parse(jsonPayload);
    
    // Return true if token is expired or will expire in the next 5 minutes
    return Date.now() >= (exp * 1000) - 5 * 60 * 1000;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true;
  }
}

// Function to refresh tokens when needed
async function ensureValidToken() {
  // Get current access token
  const currentSession = supabase.auth.session();
  const accessToken = currentSession?.access_token;
  
  // Check if token is valid
  if (!isTokenExpiring(accessToken)) {
    return accessToken;
  }
  
  // Try to refresh the token
  try {
    const refreshToken = await getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const { data, error } = await supabase.auth.refreshSession({ refresh_token: refreshToken });
    
    if (error) {
      throw error;
    }
    
    // Store new tokens
    if (data) {
      storeAuthTokens(data.access_token, data.refresh_token);
      return data.access_token;
    }
  } catch (error) {
    console.error('Failed to refresh token:', error);
    // Handle authentication error - redirect to login
    redirectToLogin();
    throw error;
  }
}
```

## Automatic Retry for Failed Requests

Implement an API client that automatically retries failed requests due to token expiration:

```javascript
// API client wrapper with automatic token refresh
class ApiClient {
  constructor() {
    this.baseUrl = 'YOUR_API_BASE_URL';
  }
  
  async fetch(endpoint, options = {}) {
    try {
      // Ensure we have a valid token before making the request
      const token = await ensureValidToken();
      
      // Add authorization header
      const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
      };
      
      // Make the API request
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers
      });
      
      // If unauthorized and we already tried refreshing, we need to log out
      if (response.status === 401) {
        // Token is invalid despite refresh attempt
        redirectToLogin();
        throw new Error('Authentication failed');
      }
      
      return response;
    } catch (error) {
      // Handle network errors or other issues
      console.error('API request failed:', error);
      throw error;
    }
  }
  
  // Convenience methods
  async get(endpoint, options = {}) {
    return this.fetch(endpoint, { ...options, method: 'GET' });
  }
  
  async post(endpoint, data, options = {}) {
    return this.fetch(endpoint, {
      ...options,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      body: JSON.stringify(data)
    });
  }
  
  // Add more methods as needed (PUT, DELETE, etc.)
}

// Usage example
const api = new ApiClient();

async function fetchUserData() {
  try {
    const response = await api.get('/api/user-profile');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    // Handle error appropriately
  }
}
```

## WebSocket Authentication Update

For applications using Supabase Realtime with WebSockets, update the authentication token when it's refreshed:

```javascript
// Function to update WebSocket authentication token
function updateWebSocketAuth(token) {
  // Update the Supabase Realtime client with new token
  supabase.realtime.setAuth(token);
}

// Modified token refresh function
async function ensureValidToken() {
  // ... existing code ...
  
  // After successfully refreshing the token:
  if (data) {
    storeAuthTokens(data.access_token, data.refresh_token);
    
    // Update WebSocket authentication
    updateWebSocketAuth(data.access_token);
    
    return data.access_token;
  }
}
```

## Handling Background Refreshing

For better user experience, implement background token refreshing:

```javascript
// Set up a timer to refresh token before it expires
function setupTokenRefreshTimer() {
  const currentSession = supabase.auth.session();
  const accessToken = currentSession?.access_token;
  
  if (!accessToken) return;
  
  try {
    // Decode token to get expiration time
    const base64Url = accessToken.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
    
    const { exp } = JSON.parse(jsonPayload);
    
    // Calculate time until token expires (in milliseconds)
    const expiresInMs = (exp * 1000) - Date.now();
    
    // Refresh token 5 minutes before it expires
    const refreshTimeMs = Math.max(0, expiresInMs - 5 * 60 * 1000);
    
    // Set up timer
    setTimeout(async () => {
      try {
        await ensureValidToken();
        // Set up next refresh
        setupTokenRefreshTimer();
      } catch (error) {
        console.error('Failed to refresh token:', error);
      }
    }, refreshTimeMs);
  } catch (error) {
    console.error('Error setting up token refresh timer:', error);
  }
}

// Call this function on login and app initialization
setupTokenRefreshTimer();
```

## Integration with Application Startup

Ensure the token refresh mechanism is initialized when your application starts:

```javascript
// Example for React application
function App() {
  useEffect(() => {
    // Initialize authentication state
    const initializeAuth = async () => {
      try {
        // Check if we have a valid token
        await ensureValidToken();
        // Set up automatic token refresh
        setupTokenRefreshTimer();
      } catch (error) {
        // If no valid token, redirect to login
        redirectToLogin();
      }
    };
    
    initializeAuth();
  }, []);
  
  // Rest of your app...
}
```

These implementations provide a robust approach to handling token refresh on the client side, ensuring a smooth user experience while maintaining security. 