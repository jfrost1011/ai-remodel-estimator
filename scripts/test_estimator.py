#!/usr/bin/env python
"""
Test script for the CostEstimator with Pinecone integration.
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

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test the CostEstimator")
    parser.add_argument(
        "--use-pinecone",
        action="store_true",
        help="Use Pinecone vector store instead of mock"
    )
    parser.add_argument(
        "--project-types",
        type=str,
        nargs="+",
        choices=["kitchen", "bathroom", "addition"],
        default=["kitchen", "bathroom"],
        help="Project types to test"
    )
    return parser.parse_args()

def main():
    """Main function to run the test."""
    args = parse_args()
    
    print("Starting CostEstimator test...")
    print(f"Using {'Pinecone' if args.use_pinecone else 'Mock'} vector store")
    
    # Set up test environment
    if not setup_test_env():
        print("Failed to set up test environment")
        return 1
    
    # Get estimator with appropriate vector store
    estimator = get_test_estimator(use_mock_vector_store=not args.use_pinecone)
    if not estimator:
        print("Failed to initialize estimator")
        return 1
    
    # Test each specified project type
    for i, project_type in enumerate(args.project_types):
        print(f"\n\nTesting Project {i+1}: {project_type} renovation")
        
        # Get test inputs for this project type
        inputs = get_test_inputs(project_type)
        print(f"Details: {json.dumps(inputs, indent=2)}")
        
        # Generate estimate
        print("\nGenerating estimate...")
        try:
            estimate = estimator.estimate(inputs)
            
            # Print results using the helper function
            print_estimate_results(estimate)
            
        except Exception as e:
            print(f"Error generating estimate for {project_type}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\nCostEstimator test completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 