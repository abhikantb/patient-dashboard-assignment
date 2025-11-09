# api_test.py

import requests
import json

# --- Configuration ---
# NOTE: Ensure your FastAPI server is running before you run this script!
API_BASE_URL = "http://127.0.0.1:8000/api/patients/"
# ---------------------

def check_api_data(url):
    print("--- Starting API Data Check ---")
    try:
        # 1. Make the GET request
        response = requests.get(url)
        
        # 2. Check the HTTP status code first
        response.raise_for_status() 
        print(f"HTTP Status Code: {response.status_code} (Success)")

        # 3. Safely parse the JSON response
        try:
            data = response.json()
            print("\n--- Raw JSON Response ---")
            # Use json.dumps for pretty printing the JSON data
            print(json.dumps(data, indent=4))
            
            # 4. Verify the top-level structure
            if 'patients' in data and isinstance(data['patients'], list):
                print("\n✅ SUCCESS: Found the 'patients' list.")
                print(f"Total records in list: {len(data['patients'])}")
            else:
                print("\n❌ WARNING: The expected 'patients' list key is missing or not a list.")
                
        except requests.exceptions.JSONDecodeError:
            print("\n❌ ERROR: Failed to decode JSON.")
            print(f"API Response Text (Check for HTML/Error message): \n{response.text[:200]}...")

    except requests.exceptions.RequestException as e:
        print("\n❌ CONNECTION FAILED:")
        print(f"Could not connect to the API server at {url}. Is Uvicorn running?")
        print(f"Details: {e}")
    
    print("\n--- Check Complete ---")

if __name__ == "__main__":
    check_api_data(API_BASE_URL)