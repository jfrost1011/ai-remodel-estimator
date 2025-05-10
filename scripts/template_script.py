"""
Template script that demonstrates the correct way to load environment variables.
Copy this template when creating new scripts that need environment variables.
"""
import os
import sys

# Add the project root to the Python path if needed
# Uncomment these lines if running the script directly and getting import errors
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the environment loader utility
from utils.env_loader import load_env_vars

def main():
    """Main function that demonstrates proper environment variable usage."""
    # Load environment variables
    if not load_env_vars():
        print("Failed to load environment variables. Exiting.")
        sys.exit(1)
    
    # Now you can safely use environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    
    # Your script logic goes here
    print("Script is running with properly loaded environment variables!")
    
    # Example of how to use the environment variables
    print(f"OpenAI API Key is {'set' if openai_api_key else 'not set'}")
    print(f"Pinecone API Key is {'set' if pinecone_api_key else 'not set'}")

if __name__ == "__main__":
    main() 