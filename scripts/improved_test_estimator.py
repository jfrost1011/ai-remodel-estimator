#!/usr/bin/env python
"""
Improved test script for CostEstimator with standardized test helpers.

This script demonstrates using the test_helpers module for consistent, 
clean testing of the CostEstimator.

Usage:
    python scripts/improved_test_estimator.py [--mock] [--project-type kitchen|bathroom|addition]

Example:
    python scripts/improved_test_estimator.py --project-type bathroom
"""
import argparse
import json
import os
import sys
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
        "--mock",
        action="store_true",
        help="Use mock vector store instead of Pinecone"
    )
    parser.add_argument(
        "--project-type",
        type=str,
        choices=["kitchen", "bathroom", "addition"],
        default="kitchen",
        help="Project type to estimate"
    )
    return parser.parse_args()

def main():
    """Main function."""
    # Parse command line arguments
    args = parse_args()
    
    print(f"=== Testing CostEstimator with {args.project_type} project ===")
    print(f"Using {'mock' if args.mock else 'real'} vector store")
    
    # Set up test environment
    if not setup_test_env():
        print("Failed to set up test environment")
        return 1
    
    # Get estimator
    estimator = get_test_estimator(use_mock_vector_store=args.mock)
    if not estimator:
        print("Failed to initialize estimator")
        return 1
    
    # Get input data
    inputs = get_test_inputs(args.project_type)
    
    # Print inputs
    print("\nInput parameters:")
    print(json.dumps(inputs, indent=2))
    
    # Generate estimate
    print("\nGenerating estimate...")
    try:
        estimate = estimator.estimate(inputs)
        
        # Print results
        print_estimate_results(estimate)
        
        # Print success message
        print("\n✅ Estimate generated successfully!")
        
        return 0
    except Exception as e:
        print(f"\n❌ Error generating estimate: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 