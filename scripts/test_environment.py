#!/usr/bin/env python
"""
Unified Environment Test Script for Renovation Estimator.

This script verifies that all necessary environment variables are properly loaded and
that API keys are valid. It replaces multiple similar scripts:
- test_keys.py
- simple_test_keys.py
- final_test_keys.py

Usage:
    python scripts/test_environment.py [--with-api-tests] [--verbose]

Options:
    --with-api-tests    Run actual API tests to verify keys work (may incur costs)
    --verbose           Show more detailed output, including key previews
"""

import os
import sys
import argparse
from typing import Dict, List, Any, Tuple, Optional

# Add project root directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import environment loader
from utils.env_loader import load_env_vars, validate_api_keys, get_api_key_status

# ANSI color codes for better output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text: str) -> None:
    """Print section header with formatting."""
    print(f"\n{BOLD}{text}{RESET}")
    print("=" * len(text))

def get_env_file_info() -> Dict[str, Any]:
    """Get information about .env file location and existence."""
    # Check different possible paths
    paths = {
        "project_root": os.path.join(project_root, ".env"),
        "renovation_estimator": os.path.join(project_root, "renovation-estimator", ".env"),
        "current_dir": ".env"
    }
    
    results = {}
    for name, path in paths.items():
        exists = os.path.exists(path)
        results[name] = {
            "path": path,
            "exists": exists,
            "size": os.path.getsize(path) if exists else None
        }
    
    return results

def test_env_loading() -> bool:
    """Test environment variable loading."""
    print_header("Testing Environment Loading")
    
    # Get info about .env file
    env_files = get_env_file_info()
    
    # Print .env file status
    print("Checking .env file locations:")
    found = False
    for name, info in env_files.items():
        status = f"{GREEN}Found{RESET}" if info["exists"] else f"{RED}Not found{RESET}"
        print(f"  {name}: {info['path']} - {status}")
        if info["exists"]:
            found = True
    
    if not found:
        print(f"{RED}No .env file found. Please create one from .env.example{RESET}")
        return False
    
    # Try to load environment variables
    print("\nLoading environment variables...")
    if load_env_vars():
        print(f"{GREEN}✓ Environment variables loaded successfully!{RESET}")
        return True
    else:
        print(f"{RED}✗ Failed to load environment variables.{RESET}")
        return False

def test_api_keys(verbose: bool = False) -> Tuple[bool, List[str]]:
    """Test that required API keys are present."""
    print_header("Checking API Keys")
    
    # Get API key status
    status = get_api_key_status(include_preview=verbose)
    
    # Required keys (add or remove as needed)
    required_keys = ["OPENAI_API_KEY", "PINECONE_API_KEY", "LANGSMITH_API_KEY"]
    
    # Print key status
    all_present = True
    missing_keys = []
    
    print("API Key Status:")
    for key, present in status.items():
        status_str = f"{GREEN}✓ Present{RESET}" if present else f"{RED}✗ Missing{RESET}"
        print(f"  {key}: {status_str}")
        
        if key in required_keys and not present:
            all_present = False
            missing_keys.append(key)
    
    # Print summary
    if all_present:
        print(f"\n{GREEN}All required API keys are present.{RESET}")
    else:
        print(f"\n{RED}Missing required API keys: {', '.join(missing_keys)}{RESET}")
    
    return all_present, missing_keys

def test_api_connectivity() -> Dict[str, bool]:
    """Test API connectivity with actual calls."""
    print_header("Testing API Connectivity")
    
    results = {}
    
    # Test OpenAI
    print("Testing OpenAI API connection...")
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini"
        )
        
        # Try a simple request
        response = llm.invoke("Hello world")
        results["openai"] = True
        print(f"{GREEN}✓ Successfully connected to OpenAI API{RESET}")
    except Exception as e:
        results["openai"] = False
        print(f"{RED}✗ Failed to connect to OpenAI API: {e}{RESET}")
    
    # Test Pinecone
    print("\nTesting Pinecone API connection...")
    try:
        from pinecone import Pinecone
        
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        indexes = pc.list_indexes()
        
        results["pinecone"] = True
        print(f"{GREEN}✓ Successfully connected to Pinecone API{RESET}")
        if indexes:
            print(f"  Found {len(indexes)} indexes: {', '.join([idx.name for idx in indexes])}")
    except Exception as e:
        results["pinecone"] = False
        print(f"{RED}✗ Failed to connect to Pinecone API: {e}{RESET}")
    
    # Test LangSmith
    print("\nTesting LangSmith API connection...")
    try:
        from langsmith import Client
        
        client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        projects = client.list_projects()
        
        results["langsmith"] = True
        print(f"{GREEN}✓ Successfully connected to LangSmith API{RESET}")
    except Exception as e:
        results["langsmith"] = False
        print(f"{RED}✗ Failed to connect to LangSmith API: {e}{RESET}")
    
    return results

def check_env_values(verbose: bool = False) -> Dict[str, Any]:
    """Check various environment values beyond API keys."""
    print_header("Checking Environment Configuration")
    
    # Non-API key configuration
    config = {
        "PINECONE_ENVIRONMENT": os.getenv("PINECONE_ENVIRONMENT"),
        "PINECONE_INDEX": os.getenv("PINECONE_INDEX"),
        "MOCK_DATA": os.getenv("MOCK_DATA"),
        "USE_PINECONE": os.getenv("USE_PINECONE"),
        "LANGSMITH_PROJECT": os.getenv("LANGSMITH_PROJECT")
    }
    
    # Default values for reference
    defaults = {
        "PINECONE_ENVIRONMENT": "us-east-1",
        "PINECONE_INDEX": "renovation-estimator",
        "MOCK_DATA": "false",
        "USE_PINECONE": "true",
        "LANGSMITH_PROJECT": "renovation-estimator"
    }
    
    # Print configuration status
    for key, value in config.items():
        # If value is present
        if value:
            # Check if it matches default
            if key in defaults and value == defaults[key]:
                print(f"  {key}: {value} {GREEN}(default){RESET}")
            else:
                print(f"  {key}: {value}")
        else:
            # Value is missing
            if key in defaults:
                print(f"  {key}: {YELLOW}Not set, using default: {defaults[key]}{RESET}")
            else:
                print(f"  {key}: {RED}Not set{RESET}")
    
    return config

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test environment setup for Renovation Estimator")
    parser.add_argument("--with-api-tests", action="store_true", help="Test API connectivity")
    parser.add_argument("--verbose", action="store_true", help="Show more detailed output")
    args = parser.parse_args()
    
    print(f"{BOLD}Renovation Estimator Environment Test{RESET}")
    print("Running comprehensive environment check...")
    
    # Print system info
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version.split()[0]}")
    
    # Test env loading
    env_ok = test_env_loading()
    if not env_ok:
        print(f"\n{RED}Environment setup failed. Please fix .env file issues.{RESET}")
        return 1
    
    # Test API keys
    keys_ok, missing_keys = test_api_keys(verbose=args.verbose)
    
    # Check other env values
    config = check_env_values(verbose=args.verbose)
    
    # Test API connectivity if requested
    api_results = None
    if args.with_api_tests:
        api_results = test_api_connectivity()
    
    # Print summary
    print_header("Summary")
    
    if env_ok and keys_ok and (not api_results or all(api_results.values())):
        print(f"{GREEN}{BOLD}✓ All tests passed!{RESET}")
        print("Environment is properly configured for the Renovation Estimator.")
        return 0
    else:
        print(f"{RED}{BOLD}✗ Some tests failed.{RESET}")
        
        if not env_ok:
            print(f"• {RED}Environment loading failed{RESET}")
        
        if not keys_ok:
            print(f"• {RED}Missing API keys: {', '.join(missing_keys)}{RESET}")
        
        if api_results and not all(api_results.values()):
            failed_apis = [api for api, success in api_results.items() if not success]
            print(f"• {RED}API connectivity issues: {', '.join(failed_apis)}{RESET}")
        
        print("\nPlease fix these issues to ensure proper functioning of the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main())