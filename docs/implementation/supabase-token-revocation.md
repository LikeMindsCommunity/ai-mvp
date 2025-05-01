# Supabase Token Revocation Research

## Summary of Findings

After researching the capabilities of Supabase for server-side token revocation, we have found that:

1. **Current Limitations**: Supabase does not currently offer a direct Admin API endpoint to revoke refresh tokens server-side. The current logout mechanism is primarily client-side, where the session is cleared locally.

2. **Session Management**: Supabase provides session management features that can be configured to limit session lifetimes:
   - Time-boxed sessions that terminate after a fixed amount of time
   - Inactivity timeouts that terminate sessions that haven't been refreshed 
   - Single-session enforcement to maintain only the most recently active session

3. **Refresh Token Security**: Supabase implements a "use once" policy for refresh tokens, where a refresh token becomes invalid after it's exchanged for a new set of tokens. This prevents replay attacks but does not allow for immediate revocation of active tokens.

4. **Session Termination Options**:
   - When a user clicks sign out locally, the session is cleared
   - When a user changes their password or performs security-sensitive actions
   - Session timeout due to inactivity
   - Session reaches maximum lifetime
   - User signs in on another device (when single session per user is enabled)

5. **Workarounds**: The suggested approach for implementing token revocation is to:
   - Use session parameters in the Supabase Auth settings to control session lifetimes
   - Implement application-level checks for sessions that should be invalidated
   - Consider using a pre-request function (as mentioned in PostgREST documentation) to check if a token has been revoked

## Implementation Recommendations

Based on our findings, we recommend the following approach for our application:

1. **Client-Side Logout**: Continue to implement client-side logout that clears local sessions.

2. **Server-Side Session Management**: 
   - Configure appropriate session timeouts in Supabase Auth settings
   - Enable "Single session per user" if appropriate for the application's security requirements
   - Consider using shorter JWT expiration times for sensitive applications

3. **Application-Level Session Tracking**:
   - Create a `revoked_sessions` table to track sessions that should be invalidated
   - Add a database function that can be called in RLS policies to check if a session has been revoked
   - Update all critical tables with RLS policies that include this check

4. **Future Improvements**:
   - Monitor Supabase's development for potential Admin API endpoints that allow direct token revocation
   - Implement more robust token validation when such features become available

## Limitations and Security Implications

- This approach does not provide immediate revocation capabilities. There will be a window of time (equal to the JWT expiration time) where a revoked token might still be valid.
- Relying on client-side logout means users must be educated on the importance of using the logout function rather than simply closing the application.
- For highly sensitive applications, shorter token lifetimes should be considered, despite the potential impact on user experience.

## References

- [Supabase User Sessions Documentation](https://supabase.com/docs/guides/auth/sessions)
- [PostgREST Token Revocation](https://postgrest.org/en/v8.0/tutorials/tut1.html#bonus-topic-immediate-revocation)
- [GitHub Discussion on API Token Management](https://github.com/orgs/supabase/discussions/3205) 