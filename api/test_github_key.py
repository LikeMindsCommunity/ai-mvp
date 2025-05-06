#!/usr/bin/env python
"""
Test script to check if the GitHub App private key is correctly loaded.
"""
import sys
import jwt
import time
import os
from api.config import get_settings

def test_private_key():
    """Test if the GitHub App private key is correctly loaded."""
    settings = get_settings()
    
    print("\n=== GitHub App Settings ===")
    print(f"GitHub App ID: {settings.github_app_id}")
    print(f"GitHub App Name: {settings.github_app_name}")
    print(f"GitHub App Slug: {settings.github_app_slug}")
    
    # Check if private key path exists
    key_path = settings.github_app_private_key_path
    print(f"\nPrivate key path: {key_path}")
    if key_path and os.path.exists(key_path):
        print(f"Private key file exists: ✅")
    else:
        print(f"Private key file doesn't exist: ❌")
    
    # Direct approach: read the key file
    private_key = None
    if key_path and os.path.exists(key_path):
        try:
            with open(key_path, "r") as f:
                private_key = f.read().strip()
            print("Successfully read private key file directly")
        except Exception as e:
            print(f"Error reading key file: {e}")
    
    # If direct reading failed, try from settings
    if not private_key:
        private_key = settings.github_app_private_key
        if private_key:
            print("Using private key from settings")
        else:
            print("\n❌ Private key is not loaded!")
            return False
    
    # Show first and last few characters of the key
    print("\n=== Private Key (truncated) ===")
    lines = private_key.strip().split('\n')
    if len(lines) > 2:
        first_50 = ''.join(lines[1:3])[:50]
        print(f"First 50 chars: {first_50}...")
        print(f"Total lines in key: {len(lines)}")
        print(f"Key starts with: {lines[0]}")
        print(f"Key ends with: {lines[-1]}")
    else:
        print(f"Key appears malformed, only {len(lines)} lines")
    
    # Try to generate a JWT
    try:
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + (10 * 60),  # 10 minutes expiration
            "iss": settings.github_app_id
        }
        
        token = jwt.encode(
            payload,
            private_key,
            algorithm="RS256"
        )
        
        print("\n=== JWT Token (truncated) ===")
        print(f"Token: {token[:50]}...")
        print("\n✅ Successfully generated JWT token!")
        return True
    except Exception as e:
        print(f"\n❌ Failed to generate JWT token: {e}")
        # Print detailed exception with more context
        import traceback
        traceback.print_exc()
        return False

def fix_jwt_key_in_env():
    """Create a fixed .env file with properly formatted JWT key."""
    settings = get_settings()
    key_path = settings.github_app_private_key_path
    if not key_path or not os.path.exists(key_path):
        print("Private key file doesn't exist, cannot fix.")
        return False
    
    try:
        # Read the current key file
        with open(key_path, "r") as f:
            private_key = f.read().strip()
        
        # Read current .env file - fix the path to be in the current directory
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        print(f"Attempting to update .env file at: {env_path}")
        
        with open(env_path, "r") as f:
            env_content = f.read()
        
        # Replace the current GITHUB_APP_PRIVATE_KEY with direct reference to file
        env_lines = env_content.split('\n')
        new_env_lines = []
        private_key_found = False
        
        for line in env_lines:
            if line.startswith("GITHUB_APP_PRIVATE_KEY="):
                private_key_found = True
                # Replace with the path reference
                new_env_lines.append(f"GITHUB_APP_PRIVATE_KEY_PATH={key_path}")
            else:
                new_env_lines.append(line)
        
        # If we didn't find the key line, add it
        if not private_key_found:
            new_env_lines.append(f"GITHUB_APP_PRIVATE_KEY_PATH={key_path}")
        
        # Write back the updated .env file
        with open(env_path, "w") as f:
            f.write('\n'.join(new_env_lines))
        
        print(f"Fixed .env file to use private key file at {key_path}")
        return True
    except Exception as e:
        print(f"Error fixing .env file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        fix_jwt_key_in_env()
    success = test_private_key()
    sys.exit(0 if success else 1) 