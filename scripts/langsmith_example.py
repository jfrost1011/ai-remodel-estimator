#!/usr/bin/env python
"""
Example script demonstrating how to use LangSmith for tracing custom functions.
"""

import os
import sys
import time
import random
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import environment variable loader
from utils.env_loader import load_env_vars

# Import LangSmith logger
from backend.langsmith_logger import get_langsmith_logger

def calculate_cost(square_feet: int, rate_per_sqft: float) -> float:
    """
    Calculate the cost of a renovation based on square footage and rate.
    This is a simple function to demonstrate LangSmith tracing.
    """
    # Simulate some processing time
    time.sleep(0.5)
    return square_feet * rate_per_sqft

def estimate_timeline(square_feet: int, complexity: str) -> int:
    """
    Estimate the timeline for a renovation in weeks.
    This is a simple function to demonstrate LangSmith tracing.
    """
    # Simulate some processing time
    time.sleep(0.5)
    
    # Base timeline based on complexity
    base_weeks = {
        "simple": 4,
        "moderate": 8,
        "complex": 12
    }.get(complexity.lower(), 6)
    
    # Add time based on square footage
    additional_weeks = square_feet // 100
    
    return base_weeks + additional_weeks

def main():
    """Example of using LangSmith to trace custom functions."""
    print("\n=== LangSmith Custom Function Tracing Example ===\n")
    
    # Load environment variables
    print("Loading environment variables...")
    if not load_env_vars():
        print("Error: Failed to load environment variables")
        return
    
    # Explicitly set LangChain environment variables
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "renovation-estimator")
    
    # Initialize LangSmith logger
    langsmith_logger = get_langsmith_logger()
    print(f"LangSmith logging enabled: {langsmith_logger.is_enabled()}")
    
    if not langsmith_logger.is_enabled():
        print("Warning: LangSmith logging is disabled. Check your API key.")
    
    # Create traced versions of our functions
    traced_calculate_cost = langsmith_logger.get_traceable_decorator(
        name="calculate_cost", 
        run_type="tool"
    )(calculate_cost)
    
    traced_estimate_timeline = langsmith_logger.get_traceable_decorator(
        name="estimate_timeline", 
        run_type="tool"
    )(estimate_timeline)
    
    # Example renovation projects
    projects = [
        {"name": "Kitchen Remodel", "square_feet": 200, "rate": 250, "complexity": "moderate"},
        {"name": "Bathroom Renovation", "square_feet": 100, "rate": 300, "complexity": "simple"},
        {"name": "Home Addition", "square_feet": 500, "rate": 200, "complexity": "complex"}
    ]
    
    # Process each project with traced functions
    for project in projects:
        print(f"\nProcessing project: {project['name']}")
        
        # Calculate cost with traced function
        cost = traced_calculate_cost(project["square_feet"], project["rate"])
        print(f"Estimated cost: ${cost:,.2f}")
        
        # Estimate timeline with traced function
        timeline = traced_estimate_timeline(project["square_feet"], project["complexity"])
        print(f"Estimated timeline: {timeline} weeks")
        
        # Record feedback (simulating user feedback)
        if langsmith_logger.is_enabled():
            # In a real application, you would get the run_id from the traced function
            # For this example, we're just simulating feedback
            satisfaction = random.uniform(0.7, 1.0)
            print(f"Simulated customer satisfaction: {satisfaction:.2f}")
            print("(Note: In a real app, you would use the actual run_id from the traced function)")
    
    print("\n=== Example Completed ===")
    print("Check your LangSmith dashboard to see the traces: https://smith.langchain.com/")

if __name__ == "__main__":
    main() 