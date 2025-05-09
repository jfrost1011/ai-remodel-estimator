import sys
import os
import json
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend components
from backend.vector_store import MockVectorStore
from backend.estimator import CostEstimator

def test_estimator():
    """Test the cost estimator functionality."""
    try:
        print("Testing cost estimator...")
        
        # Initialize components
        print("Initializing vector store...")
        vector_store = MockVectorStore()
        print("Initializing cost estimator...")
        estimator = CostEstimator(vector_store)
        
        # Test inputs
        inputs = {
            "project_type": "kitchen",
            "zip_code": "90210",
            "square_feet": 250,
            "material_grade": "premium",
            "timeline_months": 2
        }
        
        print(f"\nInput parameters:")
        print(json.dumps(inputs, indent=2))
        
        # Get estimate
        print("\nGenerating estimate...")
        estimate = estimator.estimate(inputs)
        
        print(f"\nEstimate results:")
        print(json.dumps(estimate, indent=2, default=str))
        
        if estimate and "total_range" in estimate:
            min_cost, max_cost = estimate["total_range"]
            print(f"\n✅ Estimator generated cost range: ${min_cost:,} - ${max_cost:,}")
            print(f"   Timeline: {estimate['timeline_weeks']} weeks")
            print(f"   Confidence: {estimate['confidence']*100:.1f}%")
            
            print(f"\nCost breakdown:")
            for category, amount in estimate["cost_breakdown"].items():
                print(f"   {category.capitalize()}: ${amount:,} ({amount/sum(estimate['total_range'])*200:.1f}%)")
        else:
            print("\n❌ Estimator failed to generate estimate")
    except Exception as e:
        print(f"Error running test: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_estimator() 