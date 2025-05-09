import json
import os

class MockVectorStore:
    """Simulated vector store for rapid development."""
    
    def __init__(self, data_file="data/synthetic/projects.json"):
        """Initialize with synthetic data."""
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                self.data = json.load(f)
        else:
            # Generate if not exists
            from .data_generator import generate_synthetic_data
            self.data = generate_synthetic_data()
    
    def similarity_search(self, query, filter=None, k=3):
        """Simulate vector search with pre-selected results."""
        # Extract query parameters
        project_type = self._extract_project_type(query)
        material_grade = self._extract_material_grade(query)
        
        # Filter projects
        filtered = self.data
        if project_type:
            filtered = [p for p in filtered if p["metadata"]["project_type"] == project_type]
        if material_grade:
            filtered = [p for p in filtered if p["metadata"]["material_grade"] == material_grade]
        if filter:
            for key, value in filter.items():
                filtered = [p for p in filtered if p["metadata"].get(key) == value]
        
        # Return top k results
        return filtered[:min(k, len(filtered))]
    
    def _extract_project_type(self, query):
        """Extract project type from query string."""
        query = query.lower()
        if "kitchen" in query:
            return "kitchen"
        elif "bathroom" in query:
            return "bathroom"
        elif "addition" in query or "adu" in query:
            return "addition"
        return None
    
    def _extract_material_grade(self, query):
        """Extract material grade from query string."""
        query = query.lower()
        if "premium" in query:
            return "premium"
        elif "luxury" in query:
            return "luxury"
        elif "standard" in query:
            return "standard"
        return None
