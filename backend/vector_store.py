import json
import os

class MockVectorStore:
    """Simulated vector store for rapid development."""
    
    def __init__(self, data_file=None):
        """Initialize with synthetic data."""
        # Try different file paths for the sample data
        possible_files = [
            "data/synthetic/renovation_projects.json",
            "data/synthetic/sample_projects.json",
            "data/synthetic/projects.json"
        ]
        
        # Use specified file if provided
        if data_file:
            possible_files.insert(0, data_file)
        
        # Try to load from any of the possible files
        self.data = None
        for file_path in possible_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        raw_data = json.load(f)
                    
                    # Convert to vector store format if needed
                    self.data = self._format_data(raw_data)
                    print(f"Loaded {len(self.data)} projects from {file_path}")
                    break
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        # If no file found, generate synthetic data
        if not self.data:
            print("No data files found, generating synthetic data...")
            from .data_generator import generate_projects
            raw_data = generate_projects(50)
            self.data = self._format_data(raw_data)
    
    def _format_data(self, raw_data):
        """Format raw project data for vector store format."""
        formatted_data = []
        
        for i, project in enumerate(raw_data):
            # Check if already in vector store format
            if isinstance(project, dict) and "id" in project and "metadata" in project:
                formatted_data.append(project)
                continue
            
            # Convert to vector store format
            formatted_project = {
                "id": project.get("id", f"proj-{i+1:04d}"),
                "embedding": [0.1] * 10,  # Mock embedding
                "text": (
                    f"{project.get('project_type', 'renovation')} renovation with "
                    f"{project.get('square_feet', 200)} square feet using "
                    f"{project.get('material_grade', 'standard')} materials in "
                    f"{project.get('zip_code', '00000')}"
                ),
                "metadata": project
            }
            formatted_data.append(formatted_project)
        
        return formatted_data
    
    def similarity_search(self, query, filter=None, k=3):
        """Simulate vector search with pre-selected results."""
        if not self.data:
            return []
            
        # Extract query parameters
        project_type = self._extract_project_type(query)
        material_grade = self._extract_material_grade(query)
        
        # Filter projects
        filtered = self.data
        if project_type:
            filtered = [p for p in filtered if p["metadata"].get("project_type") == project_type]
        if material_grade:
            filtered = [p for p in filtered if p["metadata"].get("material_grade") == material_grade]
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
