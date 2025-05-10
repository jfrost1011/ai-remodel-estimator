#!/usr/bin/env python
"""
Simple script to check if the Streamlit app is accessible.
"""

import requests
import time
import sys

def check_streamlit_app(url="http://localhost:8501", max_retries=5, retry_delay=2):
    """Check if the Streamlit app is accessible."""
    print(f"Checking if Streamlit app is accessible at {url}")
    
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"Success! Streamlit app is running at {url}")
                return True
            else:
                print(f"Attempt {i+1}/{max_retries}: Got status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Attempt {i+1}/{max_retries}: Connection error: {e}")
        
        if i < max_retries - 1:
            print(f"Waiting {retry_delay} seconds before retrying...")
            time.sleep(retry_delay)
    
    print("Failed to connect to the Streamlit app after multiple attempts.")
    return False

if __name__ == "__main__":
    # Try both common Streamlit ports
    if not check_streamlit_app(url="http://localhost:8501"):
        if not check_streamlit_app(url="http://localhost:8502"):
            print("Could not connect to Streamlit on either port 8501 or 8502.")
            sys.exit(1)
    
    print("Streamlit app check completed successfully.") 