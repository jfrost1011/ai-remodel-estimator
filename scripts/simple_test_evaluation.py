import sys
import os
import json
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the evaluation function
from backend.evaluation import simulate_ragas_evaluation

def test_evaluation():
    """Simple test for the RAGAS evaluation function."""
    try:
        print("Testing RAGAS evaluation...")
        
        # Test with a simple question and answer
        question = "What would a premium kitchen remodel cost for 250 sq ft?"
        answer = "Between $70,000 and $86,000."
        
        print(f"Test question: {question}")
        print(f"Test answer: {answer}")
        
        # Run the evaluation
        print("\nRunning evaluation...")
        evaluation = simulate_ragas_evaluation(question, answer)
        
        # Print results
        print("\nRAGAS Evaluation Results:")
        print(json.dumps(evaluation, indent=2, default=str))
        
        # Check if the metrics are present
        if "metrics" in evaluation:
            print("\nMetrics summary:")
            for metric, value in evaluation["metrics"].items():
                print(f"- {metric}: {value:.2f}")
        else:
            print("No metrics found in evaluation result")
            
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Error in test: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_evaluation()
    
    # Keep output visible
    input("Press Enter to continue...") 