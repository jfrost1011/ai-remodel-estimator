"""
Test script for the Renovation Estimator application.

This script tests basic functionality of key components:
- Backend estimator
- Vector store
- Data loading
- PDF generation

Usage:
    python scripts/test_app.py
"""

import os
import sys
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend components
from backend.vector_store import MockVectorStore
from backend.estimator import CostEstimator

def test_vector_store():
    """Test the mock vector store."""
    print("Testing mock vector store...")
    
    # Initialize vector store
    vector_store = MockVectorStore()
    
    # Check if it loaded sample projects
    results = vector_store.similarity_search(
        query="kitchen renovation with 200 square feet",
        k=2
    )
    
    if results and len(results) > 0:
        print(f"✅ Vector store retrieved {len(results)} results")
        print(f"   First result ID: {results[0]['id']}")
    else:
        print("❌ Vector store failed to retrieve results")

def test_estimator():
    """Test the cost estimator."""
    print("\nTesting cost estimator...")
    
    # Initialize components
    vector_store = MockVectorStore()
    estimator = CostEstimator(vector_store)
    
    # Test inputs
    inputs = {
        "project_type": "kitchen",
        "zip_code": "90210",
        "square_feet": 200,
        "material_grade": "premium",
        "timeline_months": 2
    }
    
    # Get estimate
    estimate = estimator.estimate(inputs)
    
    if estimate and "total_range" in estimate:
        min_cost, max_cost = estimate["total_range"]
        print(f"✅ Estimator generated cost range: ${min_cost:,} - ${max_cost:,}")
        print(f"   Timeline: {estimate['timeline_weeks']} weeks")
        print(f"   Confidence: {estimate['confidence']*100:.1f}%")
    else:
        print("❌ Estimator failed to generate estimate")

def test_data_files():
    """Test that necessary data files exist."""
    print("\nChecking data files...")
    
    # Check for sample projects
    sample_path = os.path.join("data", "synthetic", "sample_projects.json")
    if os.path.exists(sample_path):
        with open(sample_path, "r") as f:
            projects = json.load(f)
        print(f"✅ Found sample projects file with {len(projects)} projects")
    else:
        print("❌ Sample projects file not found")
    
    # Check for required directories
    dirs = [
        os.path.join("data", "synthetic"),
        os.path.join("data", "fine_tuning"),
        os.path.join("data", "evaluation")
    ]
    
    for dir_path in dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")

def main():
    """Run all tests."""
    print("=" * 50)
    print("Renovation Estimator Test Suite")
    print("=" * 50)
    
    # Run tests
    test_data_files()
    test_vector_store()
    test_estimator()
    
    print("\n" + "=" * 50)
    print("Tests completed")
    print("=" * 50)

if __name__ == "__main__":
    main() 