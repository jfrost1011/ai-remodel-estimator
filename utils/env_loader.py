"""
Environment variable loading utility.
Import this module in all scripts that need environment variables.
"""
import os
from dotenv import load_dotenv
import sys
from typing import List, Dict, Any, Optional, Union, Tuple

def load_env_vars():
    """
    Load environment variables from the correct location.
    Returns True if successful, False otherwise.
    """
    # Determine the correct path to .env based on current working directory
    cwd = os.getcwd()
    
    # If running from project root
    if os.path.basename(cwd) != "renovation-estimator":
        env_path = os.path.join("renovation-estimator", ".env")
    else:
        # If running from within renovation-estimator directory
        env_path = ".env"
    
    # Check if .env file exists
    if not os.path.exists(env_path):
        print(f"ERROR: .env file not found at {env_path}")
        print("Please make sure you have created a .env file with your API keys.")
        print("You can copy .env.example to .env and fill in your keys.")
        return False
    
    # Load environment variables
    load_dotenv(dotenv_path=env_path)
    
    return True

def validate_api_keys(required_keys: Optional[List[str]] = None) -> Tuple[bool, List[str]]:
    """
    Validate that required API keys are present in environment variables.
    
    Args:
        required_keys: List of required API keys to check.
                      If None, checks the standard set of keys.
    
    Returns:
        Tuple containing:
        - Boolean indicating if all required keys are present
        - List of missing keys (empty if all keys are present)
    """
    # Default required keys
    if required_keys is None:
        required_keys = [
            "OPENAI_API_KEY",
            "PINECONE_API_KEY",
            "LANGSMITH_API_KEY"
        ]
    
    # Check each required variable
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print("\nERROR: The following required environment variables are missing:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease check your .env file.")
        return False, missing_keys
    
    return True, []

def get_api_key_status(include_preview: bool = False) -> Dict[str, bool]:
    """
    Get the status of all API keys.
    
    Args:
        include_preview: Whether to include a preview of the key values
                        (first 5 characters followed by '...')
    
    Returns:
        Dictionary mapping key names to their status (boolean)
    """
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_ENVIRONMENT": os.getenv("PINECONE_ENVIRONMENT"),
        "PINECONE_INDEX": os.getenv("PINECONE_INDEX"),
        "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY"),
        "LANGSMITH_PROJECT": os.getenv("LANGSMITH_PROJECT")
    }
    
    # Create status dictionary
    status = {key: bool(value) for key, value in api_keys.items()}
    
    # Print status with previews if requested
    if include_preview:
        print("\nAPI Key Status:")
        for key, value in api_keys.items():
            preview = f"{value[:5]}..." if value else "Not set"
            if key.endswith("_KEY") and value:  # Only show preview for actual keys
                print(f"  {key}: {bool(value)} ({preview})")
            else:
                print(f"  {key}: {bool(value)}")
    
    return status

def load_and_validate_env(required_keys: Optional[List[str]] = None) -> bool:
    """
    Combined function to load environment variables and validate required keys.
    
    This is the recommended function to use in most scripts as it handles both
    loading the variables and checking that required keys are present.
    
    Args:
        required_keys: List of required API keys to check.
                      If None, checks the standard set of keys.
    
    Returns:
        Boolean indicating if environment is ready for use
    """
    # Load environment variables
    if not load_env_vars():
        return False
    
    # Validate required keys
    is_valid, _ = validate_api_keys(required_keys)
    return is_valid

# Provide a simple way to verify environment setup
if __name__ == "__main__":
    print("Testing environment variable loading...")
    
    if load_env_vars():
        print("Environment variables loaded successfully!")
        
        # Validate API keys
        is_valid, missing = validate_api_keys()
        if is_valid:
            print("All required API keys are present!")
        else:
            print(f"Missing required API keys: {', '.join(missing)}")
        
        # Display API key status with previews
        get_api_key_status(include_preview=True)
    else:
        sys.exit(1) 