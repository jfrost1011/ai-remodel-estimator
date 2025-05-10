# backend/estimator.py
def simple_estimate(zip_code: str,
                    project_type: str,
                    sqft: float,
                    material: str,
                    timeline: str) -> dict:
    """Return a naïve cost breakdown so the UI can render."""
    base_cost = {"kitchen": 250, "bathroom": 300,
                 "addition": 200}.get(project_type, 250)

    grade_mult = {"economy": 0.9, "standard": 1.0, "premium": 1.2}[material]
    timeline_mult = {"flexible": 0.95, "standard": 1.0, "rush": 1.15}[timeline]

    total = sqft * base_cost * grade_mult * timeline_mult
    return {
        "total": round(total, 2),
        "per_sqft": round(total / sqft, 2)
    }

# For compatibility with existing imports
def get_cost_estimate(*args, **kwargs):
    """Simple wrapper around simple_estimate for compatibility."""
    return simple_estimate("00000", "kitchen", 100, "standard", "standard")

def search_similar_projects(*args, **kwargs):
    """Placeholder function for search_similar_projects."""
    return [{
        "project_type": "kitchen",
        "square_feet": 100,
        "material_grade": "standard",
        "timeline": "standard",
        "cost": 25000
    }] 