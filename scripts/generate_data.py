"""
Synthetic Data Generator for Renovation Estimator

This script generates:
1. Synthetic renovation projects for the mock vector store
2. Sample data for fine-tuning
3. Test data for RAGAS evaluation

Usage:
    python generate_data.py

Generates data in the following directories:
- data/synthetic/
- data/fine_tuning/
- data/evaluation/
"""

import os
import sys
import json
import random
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend components
from backend.data_generator import generate_projects

# Directories setup
SYNTHETIC_DIR = os.path.join("data", "synthetic")
FINE_TUNING_DIR = os.path.join("data", "fine_tuning")
EVALUATION_DIR = os.path.join("data", "evaluation")

def ensure_dirs():
    """Ensure all necessary directories exist."""
    for directory in [SYNTHETIC_DIR, FINE_TUNING_DIR, EVALUATION_DIR]:
        os.makedirs(directory, exist_ok=True)

def generate_synthetic_projects(count=500):
    """Generate synthetic renovation projects."""
    print(f"Generating {count} synthetic renovation projects...")
    
    # Generate projects
    projects = generate_projects(count)
    
    # Save to JSON file
    projects_file = os.path.join(SYNTHETIC_DIR, "renovation_projects.json")
    with open(projects_file, "w") as f:
        json.dump(projects, f, indent=2)
    
    print(f"Saved {len(projects)} projects to {projects_file}")
    
    # Also save as CSV for quick inspection
    df = pd.DataFrame(projects)
    csv_file = os.path.join(SYNTHETIC_DIR, "renovation_projects.csv")
    df.to_csv(csv_file, index=False)
    
    print(f"Saved CSV version to {csv_file}")
    return projects

def generate_fine_tuning_data(projects, count=100):
    """Generate fine-tuning data from projects."""
    print(f"Generating {count} fine-tuning samples...")
    
    fine_tuning_samples = []
    selected_projects = random.sample(projects, min(count, len(projects)))
    
    for project in selected_projects:
        # Create input-output pairs for fine-tuning
        ft_sample = {
            "input": (
                f"Estimate cost for a {project['project_type']} renovation with "
                f"{project['square_feet']} square feet using {project['material_grade']} "
                f"materials in {project['zip_code']} with a timeline of "
                f"{project['timeline_months']} months."
            ),
            "output": (
                f"The estimated cost range is ${project['total_cost']-5000} to "
                f"${project['total_cost']+5000}. The breakdown includes "
                f"${int(project['total_cost']*0.4)} for materials, "
                f"${int(project['total_cost']*0.35)} for labor, "
                f"${int(project['total_cost']*0.1)} for design, "
                f"${int(project['total_cost']*0.05)} for permits, and "
                f"${int(project['total_cost']*0.1)} for contingency."
            ),
            "metadata": {
                "project_id": project["id"],
                "created_at": datetime.now().isoformat()
            }
        }
        fine_tuning_samples.append(ft_sample)
    
    # Save to JSON file
    ft_file = os.path.join(FINE_TUNING_DIR, "fine_tuning_samples.json")
    with open(ft_file, "w") as f:
        json.dump(fine_tuning_samples, f, indent=2)
    
    print(f"Saved {len(fine_tuning_samples)} fine-tuning samples to {ft_file}")
    return fine_tuning_samples

def generate_evaluation_data(projects, count=50):
    """Generate evaluation data for RAGAS metrics."""
    print(f"Generating {count} evaluation samples...")
    
    eval_samples = []
    selected_projects = random.sample(projects, min(count, len(projects)))
    
    for project in selected_projects:
        # Create evaluation samples
        eval_sample = {
            "query": (
                f"How much would it cost to renovate a {project['square_feet']} square foot "
                f"{project['project_type']} using {project['material_grade']} materials "
                f"in ZIP code {project['zip_code']}?"
            ),
            "ground_truth": (
                f"The renovation would cost approximately ${project['total_cost']} "
                f"with a breakdown of ${int(project['total_cost']*0.4)} for materials, "
                f"${int(project['total_cost']*0.35)} for labor, and "
                f"${int(project['total_cost']*0.25)} for other expenses."
            ),
            "context": json.dumps(project),
            "metadata": {
                "project_id": project["id"],
                "created_at": datetime.now().isoformat()
            }
        }
        eval_samples.append(eval_sample)
    
    # Save to JSON file
    eval_file = os.path.join(EVALUATION_DIR, "ragas_evaluation_samples.json")
    with open(eval_file, "w") as f:
        json.dump(eval_samples, f, indent=2)
    
    print(f"Saved {len(eval_samples)} evaluation samples to {eval_file}")
    return eval_samples

def main():
    """Main function to generate all data."""
    ensure_dirs()
    
    # Generate synthetic projects
    projects = generate_synthetic_projects(500)
    
    # Generate fine-tuning data
    generate_fine_tuning_data(projects, 100)
    
    # Generate evaluation data
    generate_evaluation_data(projects, 50)
    
    print("All data generation complete!")

if __name__ == "__main__":
    main() 