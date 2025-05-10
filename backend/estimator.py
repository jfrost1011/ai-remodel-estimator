# backend/estimator.py
"""
Renovation Cost Estimator Backend

This module provides cost estimation functionality for renovation projects.
"""

import os
import math
import json
from typing import Dict, Any, List, Optional

# Check if using mock data (default to True if not specified)
USE_MOCK_DATA = os.environ.get("MOCK_DATA", "true").lower() == "true"

def simple_estimate(zip_code: str,
                    project_type: str,
                    sqft: float,
                    material: str,
                    timeline: str) -> dict:
    """
    Generate a simplified renovation cost estimate based on input parameters.
    
    Args:
        zip_code: The ZIP code for the project location
        project_type: Type of renovation (kitchen, bathroom, addition)
        sqft: Square footage of the renovation
        material: Material grade (economy, standard, premium)
        timeline: Project timeline (flexible, standard, rush)
        
    Returns:
        Dictionary containing total cost and per square foot cost
    """
    # Define base costs per square foot for different project types
    base_costs = {
        "kitchen": 250,
        "bathroom": 300,
        "addition": 200,
        "basement": 150,
        "living_room": 175,
        "bedroom": 125
    }
    
    # Define multipliers for different material grades
    material_multipliers = {
        "economy": 0.8,
        "standard": 1.0,
        "premium": 1.3,
        "luxury": 1.8
    }
    
    # Define multipliers for different timelines
    timeline_multipliers = {
        "flexible": 0.9,
        "standard": 1.0,
        "rush": 1.25,
        "emergency": 1.5
    }
    
    # Define regional adjustment factors based on zip code
    # This is a simplified approach - real implementation would use a database
    region_adjustments = {
        "9": 1.3,  # California
        "1": 1.2,  # Northeast
        "3": 0.9,  # Southeast
        "7": 0.85, # Midwest
        "8": 0.95  # Mountain states
    }
    
    # Get base cost for project type (default to kitchen if not found)
    base_cost = base_costs.get(project_type, base_costs["kitchen"])
    
    # Get multipliers (default to standard if not found)
    material_mult = material_multipliers.get(material, material_multipliers["standard"])
    timeline_mult = timeline_multipliers.get(timeline, timeline_multipliers["standard"])
    
    # Get regional adjustment based on first digit of zip code
    region_mult = region_adjustments.get(zip_code[0:1], 1.0) if zip_code and zip_code[0:1].isdigit() else 1.0
    
    # Calculate total cost
    total_cost = sqft * base_cost * material_mult * timeline_mult * region_mult
    
    # Round to nearest $100
    total_cost = round(total_cost / 100) * 100
    
    # Calculate cost per square foot
    per_sqft = round(total_cost / sqft, 2)
    
    # Create a breakdown of costs
    labor_pct = 0.45
    materials_pct = 0.35
    permits_pct = 0.10
    other_pct = 0.10
    
    cost_breakdown = {
        "labor": round(total_cost * labor_pct),
        "materials": round(total_cost * materials_pct),
        "permits": round(total_cost * permits_pct),
        "other": round(total_cost * other_pct)
    }
    
    # Return the estimate
    return {
        "total": total_cost,
        "per_sqft": per_sqft,
        "breakdown": cost_breakdown,
        "currency": "USD",
        "timeline_weeks": _calculate_timeline_weeks(sqft, project_type, timeline)
    }

def _calculate_timeline_weeks(sqft: float, project_type: str, timeline: str) -> int:
    """Calculate estimated timeline in weeks based on project parameters."""
    # Base timeline in weeks for different project types
    base_timelines = {
        "kitchen": 4,
        "bathroom": 3,
        "addition": 8,
        "basement": 6,
        "living_room": 3,
        "bedroom": 2
    }
    
    # Timeline adjustments for different timelines
    timeline_adjustments = {
        "flexible": 1.2,
        "standard": 1.0,
        "rush": 0.7
    }
    
    # Get base timeline (default to kitchen if not found)
    base_weeks = base_timelines.get(project_type, base_timelines["kitchen"])
    
    # Adjust for square footage (larger projects take longer)
    size_adjustment = math.sqrt(sqft / 200)  # Scale based on sqrt of area ratio
    
    # Adjust for requested timeline
    timeline_adjustment = timeline_adjustments.get(timeline, timeline_adjustments["standard"])
    
    # Calculate final timeline
    weeks = round(base_weeks * size_adjustment * timeline_adjustment)
    
    # Ensure minimum of 1 week
    return max(1, weeks)

def get_cost_estimate(project_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Legacy function to maintain compatibility with existing code.
    Wrapper around simple_estimate that accepts a dictionary of project details.
    """
    return simple_estimate(
        project_details.get("zip_code", "00000"),
        project_details.get("project_type", "kitchen"),
        project_details.get("square_feet", 200),
        project_details.get("material_grade", "standard"),
        project_details.get("timeline", "standard")
    )

def search_similar_projects(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Search for similar renovation projects based on a query string.
    
    Args:
        query: Search query describing the project
        k: Number of results to return
        
    Returns:
        List of similar projects with metadata
    """
    # In a real implementation, this would query a vector database
    # Here we just return mock data
    sample_projects = [
        {
            "project_type": "kitchen",
            "square_feet": 200,
            "material_grade": "standard",
            "timeline": "standard",
            "total_cost": 50000,
            "location": "New York, NY",
            "completion_date": "2023-06-15"
        },
        {
            "project_type": "bathroom",
            "square_feet": 100,
            "material_grade": "premium",
            "timeline": "rush",
            "total_cost": 35000,
            "location": "Los Angeles, CA",
            "completion_date": "2023-08-20"
        },
        {
            "project_type": "addition",
            "square_feet": 400,
            "material_grade": "economy",
            "timeline": "flexible",
            "total_cost": 80000,
            "location": "Chicago, IL",
            "completion_date": "2023-05-10"
        }
    ]
    
    # Return k projects (or all if k > len(sample_projects))
    return sample_projects[:min(k, len(sample_projects))] 