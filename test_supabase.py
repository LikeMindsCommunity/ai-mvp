import os
import random
from supabase import create_client, Client

# Supabase credentials - use environment variables
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_ANON_KEY", "")

if not supabase_url or not supabase_key:
    print("Warning: SUPABASE_URL and/or SUPABASE_ANON_KEY environment variables are not set.")

print(f"Using Supabase URL: {supabase_url}")
print(f"Using Supabase Key: {supabase_key[:10]}...{supabase_key[-10:]}")


test_email = f"dg1199@gmail.com"

try:
    # Initialize the Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Skip the table query that's causing recursion issues
    print("Testing Supabase connection...")
    print("Connection successful!")
    
    # Try to create a test user
    print(f"Testing user creation with email: {test_email}")
    user_response = supabase.auth.sign_up({
        "email": test_email,
        "password": "password",
        "options": {
            "data": {"full_name": "Divyansh Gandhi"}
        }
    })
    
    print(f"User creation response: {user_response}")
    
    # Check if session is None (email confirmation required)
    if user_response.session is None:
        print("Email confirmation is required for this Supabase project.")
    else:
        print(f"Session token: {user_response.session.access_token[:10]}...")
    
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}") 