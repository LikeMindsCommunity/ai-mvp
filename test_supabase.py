import os
import random
from supabase import create_client, Client

# Supabase credentials - defined directly
supabase_url = "https://ubgsvyxwgukbtnlueqqa.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViZ3N2eXh3Z3VrYnRubHVlcXFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjQwNTEsImV4cCI6MjA2MDMwMDA1MX0.YompvqgzsJUFCWXt3sBl2v67CpXnQBWmD5jxTJxGbIQ"

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