#!/usr/bin/env python
"""
Unified Test Runner for Renovation Estimator.

This script provides a centralized way to run different types of tests:
- Environment setup tests
- Basic API integration tests
- Vector store tests
- Estimator tests
- Full system tests

Usage:
    python scripts/run_tests.py [--category all|env|api|vector|estimator|system]

Example:
    python scripts/run_tests.py --category api
"""

import os
import sys
import argparse
import time
from typing import List, Dict, Any, Callable, Optional

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import the test helpers
from scripts.test_helpers import (
    setup_test_env,
    get_test_vector_store,
    get_test_estimator,
    get_test_inputs,
    print_estimate_results
)

# ANSI color codes for pretty output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(60)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}\n")

def print_result(name: str, success: bool, duration: float) -> None:
    """Print a formatted test result."""
    status = f"{GREEN}PASSED{RESET}" if success else f"{RED}FAILED{RESET}"
    print(f"{name.ljust(30)} {status} {YELLOW}({duration:.2f}s){RESET}")

def run_test(name: str, test_func: Callable[[], bool]) -> bool:
    """Run a test function with timing and reporting."""
    print(f"Running {name}...")
    start_time = time.time()
    try:
        success = test_func()
    except Exception as e:
        print(f"{RED}Error in {name}: {e}{RESET}")
        success = False
    duration = time.time() - start_time
    print_result(name, success, duration)
    return success

# Environment Tests
def test_environment_setup() -> bool:
    """Test that the environment is set up correctly."""
    return setup_test_env(["OPENAI_API_KEY", "PINECONE_API_KEY", "LANGSMITH_API_KEY"])

# API Integration Tests
def test_openai_api() -> bool:
    """Test OpenAI API connectivity."""
    try:
        from langchain_openai import ChatOpenAI
        
        # Initialize with a simple model
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini"
        )
        
        # Try a simple query
        response = llm.invoke("What's 2+2?")
        
        # Check if we got a valid response
        return hasattr(response, "content") and response.content.strip() != ""
        
    except Exception as e:
        print(f"{RED}OpenAI API Error: {e}{RESET}")
        return False

def test_pinecone_api() -> bool:
    """Test Pinecone API connectivity."""
    try:
        from pinecone import Pinecone
        
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # List indexes to test connection
        indexes = pc.list_indexes()
        
        # Consider success if we got a response
        return True
        
    except Exception as e:
        print(f"{RED}Pinecone API Error: {e}{RESET}")
        return False

def test_langsmith_api() -> bool:
    """Test LangSmith API connectivity."""
    try:
        from langsmith import Client
        
        # Initialize LangSmith client
        client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        
        # Try to list projects
        projects = client.list_projects()
        
        # Consider success if we got a response
        return True
        
    except Exception as e:
        print(f"{RED}LangSmith API Error: {e}{RESET}")
        return False

# Vector Store Tests
def test_mock_vector_store() -> bool:
    """Test mock vector store functionality."""
    vector_store = get_test_vector_store(use_mock=True)
    if not vector_store:
        return False
    
    # Test search
    results = vector_store.similarity_search("kitchen renovation")
    return results is not None and len(results) > 0

def test_pinecone_vector_store() -> bool:
    """Test Pinecone vector store functionality."""
    # Skip if PINECONE_API_KEY is not set
    if not os.getenv("PINECONE_API_KEY"):
        print(f"{YELLOW}Skipping Pinecone test (API key not set){RESET}")
        return True
    
    try:
        vector_store = get_test_vector_store(use_mock=False)
        if not vector_store:
            return False
        
        # Test search
        results = vector_store.similarity_search("kitchen renovation")
        return results is not None
        
    except Exception as e:
        print(f"{RED}Pinecone Vector Store Error: {e}{RESET}")
        return False

# Estimator Tests
def test_cost_estimator() -> bool:
    """Test cost estimator functionality."""
    estimator = get_test_estimator(use_mock_vector_store=True)
    if not estimator:
        return False
    
    # Generate estimate
    inputs = get_test_inputs("kitchen")
    estimate = estimator.estimate(inputs)
    
    # Check if estimate has required fields
    required_fields = ["total_range", "timeline_weeks", "cost_breakdown", "confidence"]
    return all(field in estimate for field in required_fields)

# Full System Tests
def test_full_system() -> bool:
    """Test the entire system end-to-end."""
    estimator = get_test_estimator(use_mock_vector_store=True)
    if not estimator:
        return False
    
    # Test multiple project types
    project_types = ["kitchen", "bathroom", "addition"]
    all_success = True
    
    for project_type in project_types:
        print(f"Testing {project_type} project...")
        inputs = get_test_inputs(project_type)
        try:
            estimate = estimator.estimate(inputs)
            if not all(field in estimate for field in ["total_range", "timeline_weeks"]):
                print(f"{RED}Missing fields in {project_type} estimate{RESET}")
                all_success = False
        except Exception as e:
            print(f"{RED}Error in {project_type} estimate: {e}{RESET}")
            all_success = False
    
    return all_success

# Test Categories
TEST_CATEGORIES = {
    "env": [
        ("Environment Setup", test_environment_setup)
    ],
    "api": [
        ("OpenAI API", test_openai_api),
        ("Pinecone API", test_pinecone_api),
        ("LangSmith API", test_langsmith_api)
    ],
    "vector": [
        ("Mock Vector Store", test_mock_vector_store),
        ("Pinecone Vector Store", test_pinecone_vector_store)
    ],
    "estimator": [
        ("Cost Estimator", test_cost_estimator)
    ],
    "system": [
        ("Full System", test_full_system)
    ]
}

def run_test_category(category: str) -> Dict[str, bool]:
    """Run all tests in a category."""
    results = {}
    
    # Check if category exists
    if category not in TEST_CATEGORIES and category != "all":
        print(f"{RED}Unknown test category: {category}{RESET}")
        return results
    
    # Determine tests to run
    tests_to_run = []
    if category == "all":
        for cat_tests in TEST_CATEGORIES.values():
            tests_to_run.extend(cat_tests)
    else:
        tests_to_run = TEST_CATEGORIES[category]
    
    # Run tests
    for name, test_func in tests_to_run:
        success = run_test(name, test_func)
        results[name] = success
    
    return results

def main():
    """Main function to parse args and run tests."""
    parser = argparse.ArgumentParser(description="Run tests for Renovation Estimator")
    parser.add_argument(
        "--category", 
        type=str,
        default="all",
        choices=["all", "env", "api", "vector", "estimator", "system"],
        help="Test category to run"
    )
    args = parser.parse_args()
    
    print_header(f"Running {args.category.upper()} Tests")
    
    # Run tests
    results = run_test_category(args.category)
    
    # Print summary
    if results:
        print_header("Test Summary")
        
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        for name, success in results.items():
            status = f"{GREEN}PASSED{RESET}" if success else f"{RED}FAILED{RESET}"
            print(f"{name.ljust(30)} {status}")
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print(f"\n{GREEN}All tests passed!{RESET}")
            return 0
        else:
            print(f"\n{RED}Some tests failed.{RESET}")
            return 1
    else:
        print(f"{RED}No tests were run.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 