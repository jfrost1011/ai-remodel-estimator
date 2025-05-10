#!/usr/bin/env python
"""
Test script to verify Pinecone integration.
This script uses the test_helpers module for consistent testing.
"""
import os
import sys
import json
import argparse

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import test helpers
from scripts.test_helpers import setup_test_env, get_test_vector_store

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Pinecone integration")
    parser.add_argument(
        "--add-sample-data",
        action="store_true",
        help="Add sample data to the Pinecone index if it's empty"
    )
    parser.add_argument(
        "--query",
        type=str,
        default="Kitchen renovation with marble countertops",
        help="Query for similarity search"
    )
    return parser.parse_args()

def main():
    """Main function to run the test."""
    args = parse_args()
    
    print("Starting Pinecone integration test...")
    
    # Set up test environment with required Pinecone API key
    if not setup_test_env(["PINECONE_API_KEY"]):
        print("Failed to set up test environment")
        return 1
    
    # Check for Pinecone configuration
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    pinecone_index = os.getenv("PINECONE_INDEX")
    
    print(f"Pinecone Environment: {pinecone_environment}")
    print(f"Pinecone Index: {pinecone_index}")
    
    try:
        # Get the Pinecone vector store
        print("\nInitializing PineconeVectorStore...")
        # Explicitly use Pinecone (not mock)
        from backend.vector_store import PineconeVectorStore
        vector_store = PineconeVectorStore()
        
        # Get index statistics
        print("\nGetting index statistics...")
        stats = vector_store.get_stats()
        print(f"Index statistics: {stats}")
        
        # Add sample data if index is empty and requested
        if stats["total_vector_count"] == 0 and args.add_sample_data:
            print("\nIndex is empty. Adding sample data...")
            
            # Sample renovation projects
            texts = [
                "Kitchen renovation with granite countertops and stainless steel appliances, 200 sq ft, $30,000",
                "Bathroom remodel with walk-in shower and double vanity, 100 sq ft, $20,000",
                "Full house renovation including kitchen, bathrooms, and living areas, 2000 sq ft, $150,000"
            ]
            
            metadatas = [
                {"project_type": "kitchen", "square_feet": 200, "material_grade": "premium", "cost": 30000},
                {"project_type": "bathroom", "square_feet": 100, "material_grade": "premium", "cost": 20000},
                {"project_type": "full_house", "square_feet": 2000, "material_grade": "standard", "cost": 150000}
            ]
            
            ids = vector_store.add_texts(texts, metadatas)
            print(f"Added {len(ids)} sample projects with IDs: {ids}")
        else:
            print(f"\nIndex already contains {stats['total_vector_count']} vectors.")
        
        # Test similarity search
        print("\nTesting similarity search...")
        query = args.query
        print(f"Query: '{query}'")
        
        results = vector_store.similarity_search(query)
        
        print("\nSearch results:")
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Score: {result['score']}")
            print(f"Text: {result['text']}")
            print(f"Metadata: {result['metadata']}")
        
        print("\nPinecone integration test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\nError during Pinecone integration test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 