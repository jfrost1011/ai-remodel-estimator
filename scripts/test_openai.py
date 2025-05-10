#!/usr/bin/env python
"""
Test script to demonstrate OpenAI API integration.
This script uses the test_helpers module for consistent testing.
"""
import os
import sys
import argparse

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import test helpers
from scripts.test_helpers import setup_test_env

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test OpenAI API integration")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model to test"
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What's a good cost range for a 200 sqft kitchen remodel?",
        help="Query to send to the OpenAI API"
    )
    return parser.parse_args()

def main():
    """Main function to run the test."""
    args = parse_args()
    
    print("Starting OpenAI API integration test...")
    
    # Set up test environment
    if not setup_test_env(["OPENAI_API_KEY"]):
        print("Failed to set up test environment")
        return 1
    
    try:
        # Import OpenAI components
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        
        # Initialize ChatOpenAI
        print(f"\nInitializing ChatOpenAI with {args.model}...")
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=args.model
        )
        
        # Test LLM with the provided query
        print(f"Sending query to OpenAI: '{args.query}'")
        
        response = llm.invoke(args.query)
        print("\nLLM Response:")
        print(response.content)
        
        # Initialize OpenAIEmbeddings
        print("\nInitializing OpenAIEmbeddings with text-embedding-3-small...")
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
        
        # Test embeddings with a simple text
        text = "Kitchen remodel with granite countertops"
        print(f"Generating embeddings for: '{text}'")
        
        embedding = embeddings.embed_query(text)
        print(f"Successfully generated embedding with {len(embedding)} dimensions")
        print(f"First 5 values: {embedding[:5]}")
        
        print("\nOpenAI API integration test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\nError during OpenAI API integration test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 