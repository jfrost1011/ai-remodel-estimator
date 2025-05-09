import json
import random
import os
from datetime import datetime

"""
Synthetic Data Generator for Renovation Cost Estimator

This module generates realistic synthetic data for renovation projects,
which serves as the foundation for the RAG-based cost estimation system.
The data includes various project types, realistic square footage ranges,
material grades, and location-based cost variations.

Key features:
- Generates diverse renovation project types (kitchen, bathroom, addition)
- Creates realistic cost variations based on project parameters
- Produces structured data with detailed metadata
- Generates detailed cost breakdowns by category
- Supports persistence to JSON for vector store retrieval
"""

def generate_synthetic_data(count=20):
    """Generate synthetic renovation projects.
    
    Creates a specified number of synthetic renovation projects with realistic
    parameters and cost calculations. Each project includes detailed metadata
    suitable for vector storage and retrieval.
    
    Args:
        count (int): Number of synthetic projects to generate
        
    Returns:
        list: Collection of generated project objects
    """
    project_types = ["kitchen", "bathroom", "addition"]
    material_grades = ["standard", "premium", "luxury"]
    zip_codes = ["90210", "10001", "60601", "98101", "33139"]
    
    projects = []
    
    # Create synthetic projects
    for i in range(count):
        project_type = random.choice(project_types)
        
        # Set realistic ranges based on project type
        if project_type == "kitchen":
            sqft_range = (100, 300)
            cost_per_sqft = random.uniform(150, 350)
            timeline_range = (4, 12)
        elif project_type == "bathroom":
            sqft_range = (40, 150)
            cost_per_sqft = random.uniform(200, 400)
            timeline_range = (3, 8)
        else:  # addition
            sqft_range = (200, 800)
            cost_per_sqft = random.uniform(200, 500)
            timeline_range = (8, 20)
        
        # Generate random values
        sqft = random.randint(*sqft_range)
        material = random.choice(material_grades)
        zip_code = random.choice(zip_codes)
        
        # Calculate costs with material multiplier
        multipliers = {"standard": 1.0, "premium": 1.5, "luxury": 2.0}
        multiplier = multipliers[material]
        base_cost = int(sqft * cost_per_sqft * multiplier)
        
        # Create breakdown
        breakdown = {
            "materials": int(base_cost * 0.4),
            "labor": int(base_cost * 0.35),
            "permits": int(base_cost * 0.05),
            "design": int(base_cost * 0.1),
            "contingency": int(base_cost * 0.1)
        }
        
        # Create project
        project = {
            "id": f"proj_{i}",
            "text": f"{project_type} renovation with {sqft} square feet using {material} materials in {zip_code}. Total cost: ${base_cost}.",
            "metadata": {
                "project_type": project_type,
                "square_feet": sqft,
                "material_grade": material,
                "zip_code": zip_code,
                "total_cost": base_cost,
                "cost_breakdown": breakdown,
                "timeline_weeks": random.randint(*timeline_range),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        projects.append(project)
    
    # Save to file
    os.makedirs("data/synthetic", exist_ok=True)
    with open("data/synthetic/projects.json", "w") as f:
        json.dump(projects, f, indent=2)
    
    return projects

# Generate data when module is run directly
if __name__ == "__main__":
    projects = generate_synthetic_data(20)
    print(f"Generated {len(projects)} synthetic projects")
