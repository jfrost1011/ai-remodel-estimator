"""
Data loading utility for the Renovation Estimator project.
Provides centralized data loading functionality to avoid code duplication.

This module handles:
- Loading project data from JSON files
- Searching multiple file paths
- Generating synthetic data when needed
- Formatting data consistently for vector stores
"""
import os
import json
import sys
from typing import List, Dict, Any, Optional, Union

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_project_data(
    data_file: Optional[str] = None,
    fallback_to_synthetic: bool = True,
    count: int = 20,
    return_formatted: bool = True
) -> List[Dict[str, Any]]:
    """
    Load renovation project data from file or generate synthetic data.
    
    Args:
        data_file: Optional path to specific data file
        fallback_to_synthetic: Whether to generate synthetic data if file not found
        count: Number of synthetic projects to generate if needed
        return_formatted: Whether to return data in vector store format
        
    Returns:
        List of project dictionaries
    """
    # Try different file paths
    possible_files = [
        "data/synthetic/renovation_projects.json",
        "data/synthetic/sample_projects.json",
        "data/synthetic/projects.json"
    ]
    
    if data_file:
        possible_files.insert(0, data_file)
    
    # Try to load data from files
    raw_data = None
    used_file = None
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    raw_data = json.load(f)
                used_file = file_path
                print(f"Loaded {len(raw_data)} projects from {file_path}")
                break
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    # Generate synthetic data if needed
    if raw_data is None and fallback_to_synthetic:
        print("No data files found, generating synthetic data...")
        try:
            from backend.data_generator import generate_synthetic_data
            raw_data = generate_synthetic_data(count)
            print(f"Generated {len(raw_data)} synthetic projects")
        except ImportError:
            print("WARNING: Could not import data_generator. No data available.")
            return []
    
    # Return early if no data
    if not raw_data:
        return []
    
    # Format if requested
    if return_formatted:
        return format_data_for_vector_store(raw_data)
    
    return raw_data

def format_data_for_vector_store(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format raw project data for vector store format.
    
    Args:
        raw_data: List of project dictionaries
        
    Returns:
        List of formatted projects with id, text, and metadata fields
    """
    formatted_data = []
    
    for i, project in enumerate(raw_data):
        # Check if already in vector store format
        if isinstance(project, dict) and "id" in project and "metadata" in project:
            formatted_data.append(project)
            continue
        
        # Generate project ID if not present
        project_id = project.get("id", f"proj-{i+1:04d}")
        
        # Extract or generate project description
        project_type = project.get("project_type", "renovation")
        square_feet = project.get("square_feet", 200)
        material_grade = project.get("material_grade", "standard")
        
        # Create text representation
        text = (
            f"{project_type} renovation with "
            f"{square_feet} square feet using "
            f"{material_grade} materials"
        )
        
        # Add location if available
        if "zip_code" in project:
            text += f" in {project.get('zip_code')}"
        
        # Format for vector store
        formatted_project = {
            "id": project_id,
            "text": text,
            "metadata": project
        }
        
        formatted_data.append(formatted_project)
    
    return formatted_data

def save_project_data(data: List[Dict[str, Any]], file_path: str) -> bool:
    """
    Save project data to a JSON file.
    
    Args:
        data: List of project dictionaries
        file_path: Path to save the data
        
    Returns:
        True if successful, False otherwise
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} projects to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")
        return False

# Simple test function
if __name__ == "__main__":
    print("Testing data loader...")
    
    # Test loading data
    projects = load_project_data()
    print(f"Loaded {len(projects)} projects")
    
    if projects:
        # Show first project
        print("\nSample project:")
        print(json.dumps(projects[0], indent=2)) 