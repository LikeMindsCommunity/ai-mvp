# Authentication Security Guidelines

## Logout Limitations

Users should be aware of the following limitations regarding the logout functionality in our application:

### How Logout Works

When you click the "Logout" button in our application:

1. Your local session is cleared (including tokens stored in your browser)
2. The application redirects you to the login page
3. The server receives a logout request, which attempts to invalidate your session

However, there are some technical limitations to be aware of:

- **Session Persistence**: Due to the nature of JSON Web Tokens (JWTs), your access token may remain valid for a short period after logout (typically up to 1 hour, depending on configuration).
- **Best-Effort Revocation**: The logout process is "best-effort" - we cannot guarantee immediate invalidation of all active sessions across all devices.
- **Multiple Devices**: If you're logged in on multiple devices, logging out on one device may not immediately affect your sessions on other devices.

### Security Recommendations

To ensure maximum security when using our application:

1. **Always Use the Logout Button**
   - Never simply close the application or browser window without logging out properly
   - This ensures your local session is cleared and the server is notified

2. **Secure Your Device**
   - Use password protection, biometric authentication, and screen locks on all devices
   - Don't leave your device unattended while logged into the application

3. **Be Aware of Session Duration**
   - Your session will automatically expire after a period of inactivity (typically 24 hours)
   - For security-sensitive operations, the application may require re-authentication

4. **Password Security**
   - If you suspect unauthorized access, change your password immediately
   - Changing your password will invalidate all active sessions across all devices
   - Use a strong, unique password for your account

5. **Public Computers**
   - Avoid using the application on public or shared computers when possible
   - If you must use a public computer, always log out and clear the browser cache when finished

6. **Report Suspicious Activity**
   - If you notice any unusual activity on your account, report it immediately
   - Check your account's recent activity if available

### Special Considerations for Sensitive Data

If you're working with particularly sensitive data within our application:

1. **Shorter Sessions**: Consider logging out and back in more frequently
2. **Device Limitations**: Limit the number of devices where you access the application
3. **Regular Verification**: Periodically check which devices have active sessions if this feature is available

By understanding these limitations and following these guidelines, you can help ensure the security of your account and data while using our application. 