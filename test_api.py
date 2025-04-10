import requests
import time
import json

def test_api_root():
    """Test the API server root endpoint and print detailed information about the response or errors."""
    url = "http://localhost:8001/"
    try:
        print(f"\n=== Testing root endpoint: {url} ===")
        response = requests.get(url, timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        # Get more details about the error
        if hasattr(e, 'errno'):
            print(f"Error number: {e.errno}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_test_endpoint():
    """Test the API simple test endpoint that doesn't use external dependencies."""
    url = "http://localhost:8001/api/v1/test"
    try:
        print(f"\n=== Testing simple test endpoint: {url} ===")
        response = requests.get(url, timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_generate():
    """Test the API generate endpoint and print detailed information about the response or errors."""
    url = "http://localhost:8001/api/v1/generate"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "Create a simple Flutter counter app",
        "project_id": None
    }
    
    try:
        print(f"\n=== Testing generate endpoint: {url} ===")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            print("Request successful!")
            print(f"Response content (truncated): {response.text[:300]}...")
        else:
            print(f"Request failed with status {response.status_code}")
            print(f"Response content: {response.text}")
        
        return response.status_code == 200
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test root endpoint
    root_success = test_api_root()
    
    # Test simple test endpoint
    test_endpoint_success = test_api_test_endpoint()
    
    # Test generate endpoint (optional)
    generate_test = False  # Set to True to also test the generate endpoint
    if generate_test:
        generate_success = test_api_generate()
    else:
        generate_success = None
    
    # Print summary
    print("\n=== Test Results ===")
    print(f"Root endpoint: {'✓ SUCCESS' if root_success else '✗ FAILED'}")
    print(f"Test endpoint: {'✓ SUCCESS' if test_endpoint_success else '✗ FAILED'}")
    if generate_success is not None:
        print(f"Generate endpoint: {'✓ SUCCESS' if generate_success else '✗ FAILED'}")
    else:
        print("Generate endpoint: SKIPPED")
    
    # Exit with status code
    import sys
    sys.exit(0 if root_success and test_endpoint_success else 1) 