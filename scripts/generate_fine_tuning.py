import os
import json
import pandas as pd
import random
from datetime import datetime

def generate_embedding_training_data():
    """Prepare training data for embedding fine-tuning."""
    # Load synthetic data
    try:
        with open("data/synthetic/projects.json", "r") as f:
            projects = json.load(f)
    except FileNotFoundError:
        from backend.data_generator import generate_synthetic_data
        projects = generate_synthetic_data()
    
    # Create training examples
    train_pairs = []
    
    for i, project in enumerate(projects):
        # Extract metadata
        metadata = project["metadata"]
        
        # Create query
        query = f"{metadata['project_type']} renovation with {metadata['square_feet']} sq ft using {metadata['material_grade']} materials"
        
        # Create document
        document = project["text"]
        
        # Add positive pair
        train_pairs.append({
            "query": query,
            "context": document,
            "relevance": 1.0
        })
        
        # Add negative pairs (different project types)
        negative_projects = [p for p in projects if p["metadata"]["project_type"] != metadata["project_type"]]
        if negative_projects:
            neg_project = random.choice(negative_projects)
            train_pairs.append({
                "query": query,
                "context": neg_project["text"],
                "relevance": 0.0
            })
    
    # Save training data as CSV
    os.makedirs("data/fine_tuning", exist_ok=True)
    
    df = pd.DataFrame([{
        "text_1": pair["query"],
        "text_2": pair["context"],
        "label": pair["relevance"]
    } for pair in train_pairs])
    
    csv_path = "data/fine_tuning/train_pairs.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved fine-tuning data at {csv_path}")
    
    # Copy to certification directory
    os.makedirs("certification/task6_7_fine_tuning", exist_ok=True)
    df.to_csv("certification/task6_7_fine_tuning/train_pairs.csv", index=False)
    
    # Create AutoTrain script
    autotrain_script = f"""
    autotrain dream \\
        --model sentence-transformers/all-MiniLM-L6-v2 \\
        --data {csv_path} \\
        --project-name renovation-embeddings
    """
    
    autotrain_script_path = "scripts/run_autotrain.sh"
    with open(autotrain_script_path, "w") as f:
        f.write(autotrain_script)
    
    print(f"Generated AutoTrain script at {autotrain_script_path}")
    
    # Make script executable
    try:
        os.chmod(autotrain_script_path, 0o755)
    except:
        print("Note: Could not make script executable on Windows")
    
    return csv_path

if __name__ == "__main__":
    generate_embedding_training_data()
    print("Fine-tuning data generation complete!") 