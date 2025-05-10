#!/usr/bin/env python
"""
Test script for LangSmith integration with the renovation estimator.
This script uses the test_helpers module for consistent testing.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import test helpers
from scripts.test_helpers import (
    setup_test_env,
    get_test_estimator,
    get_test_inputs,
    print_estimate_results
)

# Import LangSmith logger for direct testing
from backend.langsmith_logger import get_langsmith_logger, test_langsmith_logger

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test LangSmith integration")
    parser.add_argument(
        "--project-type",
        type=str,
        choices=["kitchen", "bathroom", "addition"],
        default="kitchen",
        help="Project type to test"
    )
    parser.add_argument(
        "--test-direct",
        action="store_true",
        help="Test the LangSmith logger directly"
    )
    return parser.parse_args()

def main():
    """Run the LangSmith integration test."""
    args = parse_args()
    
    print("\n=== Starting LangSmith Integration Test ===\n")
    
    # Set up test environment
    if not setup_test_env(["OPENAI_API_KEY", "LANGSMITH_API_KEY"]):
        print("Failed to set up test environment (Warning: LANGSMITH_API_KEY may be optional)")
    
    # Explicitly set LangChain environment variables
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "renovation-estimator")
    
    # Check for LangSmith API key
    if not os.environ.get("LANGSMITH_API_KEY"):
        print("Warning: LANGSMITH_API_KEY not found. LangSmith logging will be disabled.")
    else:
        print(f"LangSmith API key found: {os.environ.get('LANGSMITH_API_KEY')[:10]}...")
        print(f"LangSmith project: {os.environ.get('LANGSMITH_PROJECT')}")
    
    # Test the LangSmith logger directly if requested
    if args.test_direct:
        print("\n--- Testing LangSmith Logger Directly ---")
        test_langsmith_logger()
    
    # Test CostEstimator with LangSmith tracing
    print("\n--- Testing CostEstimator with LangSmith Tracing ---")
    try:
        # Get estimator using the helper
        estimator = get_test_estimator(use_mock_vector_store=True)
        if not estimator:
            print("Failed to initialize estimator")
            return 1
        
        # Get input data for the specified project type
        input_data = get_test_inputs(args.project_type)
        
        print(f"\nGenerating estimate for: {json.dumps(input_data, indent=2)}")
        
        # Generate the estimate (this should be traced by LangSmith)
        estimate = estimator.estimate(input_data)
        
        # Print the results using the helper
        print_estimate_results(estimate)
        
    except Exception as e:
        print(f"Error during CostEstimator test: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n=== LangSmith Integration Test Completed ===")
    print("View your traces at: https://smith.langchain.com/")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 