"""
Test Helpers for Renovation Estimator.

This module provides common utilities for test scripts to reduce code duplication and
ensure consistent test setup across the project.

Usage:
    from scripts.test_helpers import setup_test_env, get_test_estimator, etc.
"""
import os
import sys
import json
import traceback
from typing import Dict, Any, Optional, Tuple, List

# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

def setup_test_env(required_keys: Optional[List[str]] = None) -> bool:
    """
    Set up the test environment with proper imports and environment variables.
    
    Args:
        required_keys: List of environment variables that must be present
                      Defaults to ["OPENAI_API_KEY", "PINECONE_API_KEY"]
                      
    Returns:
        True if setup was successful, False otherwise
    """
    print(f"Setting up test environment...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Set default required keys if not provided
    if required_keys is None:
        required_keys = ["OPENAI_API_KEY", "PINECONE_API_KEY"]
    
    try:
        # Import environment variable loader
        from utils.env_loader import load_env_vars
        print("Successfully imported utils.env_loader")
        
        # Load environment variables
        if not load_env_vars():
            print("Failed to load environment variables. Exiting.")
            return False
        
        # Check for required keys
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"Missing required API keys: {', '.join(missing_keys)}")
            return False
        
        print("Environment variables loaded successfully!")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return False

def get_test_vector_store(use_mock: bool = True):
    """
    Get a vector store instance for testing.
    
    Args:
        use_mock: Whether to use the mock vector store (True) or real Pinecone (False)
        
    Returns:
        A vector store instance or None if initialization fails
    """
    try:
        # Import vector store implementation
        from backend.vector_store import get_vector_store
        
        # Create vector store
        vector_store = get_vector_store(use_mock=use_mock)
        print(f"Successfully created {'mock' if use_mock else 'real'} vector store")
        return vector_store
        
    except Exception as e:
        print(f"Error creating vector store: {e}")
        traceback.print_exc()
        return None

def get_test_estimator(use_mock_vector_store: bool = True):
    """
    Get a cost estimator instance for testing.
    
    Args:
        use_mock_vector_store: Whether to use mock vector store
        
    Returns:
        A CostEstimator instance or None if initialization fails
    """
    try:
        # Import CostEstimator
        from backend.estimator import CostEstimator
        
        # Get vector store
        vector_store = get_test_vector_store(use_mock=use_mock_vector_store)
        if not vector_store:
            print("Failed to create vector store")
            return None
        
        # Create estimator
        estimator = CostEstimator(vector_store)
        print("Successfully created CostEstimator")
        return estimator
        
    except Exception as e:
        print(f"Error creating estimator: {e}")
        traceback.print_exc()
        return None

def get_test_inputs(project_type: str = "kitchen") -> Dict[str, Any]:
    """
    Get standard test inputs for cost estimation.
    
    Args:
        project_type: Type of renovation project
        
    Returns:
        Dictionary of test inputs
    """
    # Default parameters
    params = {
        "kitchen": {
            "square_feet": 200,
            "material_grade": "premium",
            "zip_code": "10001",
            "timeline_months": 2
        },
        "bathroom": {
            "square_feet": 100,
            "material_grade": "luxury",
            "zip_code": "90210",
            "timeline_months": 1
        },
        "addition": {
            "square_feet": 500,
            "material_grade": "standard",
            "zip_code": "60601",
            "timeline_months": 3
        }
    }
    
    # Get parameters for specified project type
    project_params = params.get(project_type, params["kitchen"])
    
    # Create full input dictionary
    inputs = {
        "project_type": project_type,
        **project_params
    }
    
    return inputs

def print_estimate_results(estimate: Dict[str, Any]) -> None:
    """
    Print formatted results of a cost estimate.
    
    Args:
        estimate: Dictionary containing cost estimate data
    """
    if not estimate:
        print("No estimate data to display")
        return
    
    # Print basic estimate data
    print("\nEstimate Results:")
    print(json.dumps(estimate, indent=2))
    
    # Print formatted summary
    if "total_range" in estimate:
        min_cost, max_cost = estimate["total_range"]
        print(f"\nEstimated Cost: ${min_cost:,} - ${max_cost:,}")
        print(f"Timeline: {estimate.get('timeline_weeks', 'N/A')} weeks")
        print(f"Confidence: {estimate.get('confidence', 0) * 100:.1f}%")
        
        # Print breakdown if available
        if "cost_breakdown" in estimate:
            print("\nCost Breakdown:")
            for category, amount in estimate["cost_breakdown"].items():
                print(f"  {category.title()}: ${amount:,}")

def run_basic_test():
    """Run a basic test of the test helper functions."""
    if not setup_test_env():
        print("Test environment setup failed")
        return False
    
    estimator = get_test_estimator(use_mock_vector_store=True)
    if not estimator:
        print("Failed to create estimator")
        return False
    
    inputs = get_test_inputs("kitchen")
    print(f"\nUsing test inputs:")
    print(json.dumps(inputs, indent=2))
    
    try:
        estimate = estimator.estimate(inputs)
        print_estimate_results(estimate)
        print("\nTest completed successfully!")
        return True
    except Exception as e:
        print(f"Error during test: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing the test helpers...")
    run_basic_test() 