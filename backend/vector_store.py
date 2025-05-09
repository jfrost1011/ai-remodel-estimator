import json
import os
import numpy as np
from typing import List, Dict, Any, Optional

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
            from .data_generator import generate_synthetic_data
            raw_data = generate_synthetic_data(50)
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


class OpenAIVectorStore:
    """Real vector store implementation using OpenAI embeddings."""
    
    def __init__(self, data_file=None):
        """Initialize with data from file and OpenAI embeddings."""
        try:
            from openai import OpenAI
            import numpy as np
        except ImportError:
            raise ImportError("OpenAI package not found. Install with 'pip install openai'")
        
        # Check for API key
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Set embedding model
        self.embedding_model = "text-embedding-3-small"
        
        # Load or generate data
        self.data = self._load_data(data_file)
        
        # Generate embeddings if not already present
        self._ensure_embeddings()
    
    def _load_data(self, data_file):
        """Load data from file or generate synthetic data."""
        # Try different file paths
        possible_files = [
            "data/synthetic/renovation_projects.json",
            "data/synthetic/sample_projects.json",
            "data/synthetic/projects.json"
        ]
        
        if data_file:
            possible_files.insert(0, data_file)
        
        # Try to load data
        data = None
        for file_path in possible_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        raw_data = json.load(f)
                    
                    data = self._format_data(raw_data)
                    print(f"Loaded {len(data)} projects from {file_path}")
                    break
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        # Generate data if none found
        if not data:
            print("No data files found, generating synthetic data...")
            from .data_generator import generate_synthetic_data
            raw_data = generate_synthetic_data(20)
            data = self._format_data(raw_data)
        
        return data
    
    def _format_data(self, raw_data):
        """Format data for vector storage."""
        formatted_data = []
        
        for i, project in enumerate(raw_data):
            # Check if already in correct format
            if isinstance(project, dict) and "id" in project and "metadata" in project:
                # Make sure there's a text field for embedding
                if "text" not in project:
                    project["text"] = (
                        f"{project['metadata'].get('project_type', 'renovation')} renovation with "
                        f"{project['metadata'].get('square_feet', 200)} square feet using "
                        f"{project['metadata'].get('material_grade', 'standard')} materials"
                    )
                formatted_data.append(project)
                continue
            
            # Convert to vector store format
            formatted_project = {
                "id": project.get("id", f"proj-{i+1:04d}"),
                "text": (
                    f"{project.get('project_type', 'renovation')} renovation with "
                    f"{project.get('square_feet', 200)} square feet using "
                    f"{project.get('material_grade', 'standard')} materials"
                ),
                "metadata": project
            }
            formatted_data.append(formatted_project)
        
        return formatted_data
    
    def _ensure_embeddings(self):
        """Generate embeddings for all data points if not present."""
        needs_embedding = [doc for doc in self.data if "embedding" not in doc]
        
        if needs_embedding:
            print(f"Generating embeddings for {len(needs_embedding)} documents...")
            
            # Process in batches to avoid rate limits
            batch_size = 5
            for i in range(0, len(needs_embedding), batch_size):
                batch = needs_embedding[i:i+batch_size]
                
                # Get text for embedding
                texts = [doc["text"] for doc in batch]
                
                # Generate embeddings
                try:
                    response = self.client.embeddings.create(
                        model=self.embedding_model,
                        input=texts
                    )
                    
                    # Add embeddings to documents
                    for j, embedding_data in enumerate(response.data):
                        batch[j]["embedding"] = embedding_data.embedding
                except Exception as e:
                    print(f"Error generating embeddings: {e}")
                    # Add placeholder embeddings if API call fails
                    for doc in batch:
                        doc["embedding"] = [0.1] * 1536  # Typical OpenAI embedding size
            
            print("Embedding generation complete")
            
            # Save embeddings to disk for future use
            self._save_embeddings()
    
    def _save_embeddings(self):
        """Save data with embeddings to disk."""
        os.makedirs("data/embeddings", exist_ok=True)
        
        # Filter out the embedding vectors to save disk space
        save_data = []
        for doc in self.data:
            doc_copy = doc.copy()
            if "embedding" in doc_copy:
                # Convert numpy arrays to lists for JSON serialization
                if isinstance(doc_copy["embedding"], np.ndarray):
                    doc_copy["embedding"] = doc_copy["embedding"].tolist()
            save_data.append(doc_copy)
        
        with open("data/embeddings/embedded_projects.json", "w") as f:
            json.dump(save_data, f)
    
    def similarity_search(self, query: str, filter: Optional[Dict[str, Any]] = None, k: int = 3) -> List[Dict]:
        """Search for documents similar to the query."""
        # Generate embedding for query
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=[query]
            )
            query_embedding = response.data[0].embedding
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []
        
        # Filter documents if filter is provided
        filtered_docs = self.data
        if filter:
            filtered_docs = [
                doc for doc in filtered_docs 
                if all(doc["metadata"].get(key) == value for key, value in filter.items())
            ]
        
        # Calculate cosine similarity
        results = []
        for doc in filtered_docs:
            if "embedding" in doc:
                # Calculate cosine similarity
                doc_embedding = doc["embedding"]
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                
                # Add to results with similarity score
                doc_with_score = doc.copy()
                doc_with_score["similarity"] = similarity
                results.append(doc_with_score)
        
        # Sort by similarity (descending) and return top k
        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return results[:k]
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


class PineconeVectorStore:
    """Vector store implementation using Pinecone as the backend and OpenAI embeddings."""
    
    def __init__(self, data_file=None):
        """Initialize with data from file, OpenAI embeddings, and Pinecone storage."""
        # Check for required packages
        try:
            from openai import OpenAI
            from pinecone import Pinecone, PodSpec
        except ImportError:
            raise ImportError("Required packages not found. Install with 'pip install openai pinecone-client'")
        
        # Check for API keys
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        self.pinecone_environment = os.environ.get("PINECONE_ENVIRONMENT")
        self.pinecone_index_name = os.environ.get("PINECONE_INDEX", "renovation-estimator")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        if not self.pinecone_api_key:
            raise ValueError("Pinecone API key not found in environment variables")
        if not self.pinecone_environment:
            raise ValueError("Pinecone environment not found in environment variables")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Set embedding model
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536  # Dimension for text-embedding-3-small
        
        # Initialize Pinecone
        self.pinecone = Pinecone(api_key=self.pinecone_api_key)
        
        # Check if index exists, create if not
        try:
            indexes = self.pinecone.list_indexes()
            if self.pinecone_index_name not in [index.name for index in indexes]:
                print(f"Creating Pinecone index '{self.pinecone_index_name}'...")
                self.pinecone.create_index(
                    name=self.pinecone_index_name,
                    dimension=self.embedding_dimension,
                    metric="cosine",
                    spec=PodSpec(environment=self.pinecone_environment)
                )
            
            # Connect to index
            self.index = self.pinecone.Index(self.pinecone_index_name)
            print(f"Connected to Pinecone index '{self.pinecone_index_name}'")
            
            # Check if we need to populate the index
            stats = self.index.describe_index_stats()
            vector_count = stats.namespaces[""].vector_count if "" in stats.namespaces else 0
            
            if vector_count == 0:
                print("Index is empty, loading initial data...")
                self._load_and_index_data(data_file)
            else:
                print(f"Index already contains {vector_count} vectors")
        
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            raise
    
    def _load_and_index_data(self, data_file):
        """Load data and index it in Pinecone."""
        # Try different file paths
        possible_files = [
            "data/synthetic/renovation_projects.json",
            "data/synthetic/sample_projects.json",
            "data/synthetic/projects.json"
        ]
        
        if data_file:
            possible_files.insert(0, data_file)
        
        # Try to load data
        raw_data = None
        for file_path in possible_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        raw_data = json.load(f)
                    print(f"Loaded {len(raw_data)} projects from {file_path}")
                    break
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        # Generate data if none found
        if not raw_data:
            print("No data files found, generating synthetic data...")
            from .data_generator import generate_synthetic_data
            raw_data = generate_synthetic_data(20)
        
        # Process and index the data
        self._index_data(raw_data)
    
    def _index_data(self, raw_data):
        """Generate embeddings and index the data in Pinecone."""
        # Format data
        formatted_data = []
        for i, project in enumerate(raw_data):
            # Check if already in vector store format
            if isinstance(project, dict) and "id" in project and "metadata" in project:
                # Make sure there's a text field for embedding
                if "text" not in project:
                    project["text"] = (
                        f"{project['metadata'].get('project_type', 'renovation')} renovation with "
                        f"{project['metadata'].get('square_feet', 200)} square feet using "
                        f"{project['metadata'].get('material_grade', 'standard')} materials"
                    )
                formatted_data.append(project)
            else:
                # Convert to vector store format
                formatted_project = {
                    "id": project.get("id", f"proj-{i+1:04d}"),
                    "text": (
                        f"{project.get('project_type', 'renovation')} renovation with "
                        f"{project.get('square_feet', 200)} square feet using "
                        f"{project.get('material_grade', 'standard')} materials"
                    ),
                    "metadata": project
                }
                formatted_data.append(formatted_project)
        
        # Process in batches to avoid rate limits
        batch_size = 5
        for i in range(0, len(formatted_data), batch_size):
            batch = formatted_data[i:i+batch_size]
            
            # Get text for embedding
            texts = [doc["text"] for doc in batch]
            
            # Generate embeddings
            try:
                response = self.openai_client.embeddings.create(
                    model=self.embedding_model,
                    input=texts
                )
                
                # Prepare vectors for Pinecone
                vectors_to_upsert = []
                for j, embedding_data in enumerate(response.data):
                    doc = batch[j]
                    vectors_to_upsert.append({
                        "id": doc["id"],
                        "values": embedding_data.embedding,
                        "metadata": {
                            "text": doc["text"],
                            "project_type": doc["metadata"].get("project_type", ""),
                            "square_feet": doc["metadata"].get("square_feet", 0),
                            "material_grade": doc["metadata"].get("material_grade", ""),
                            "total_cost": doc["metadata"].get("total_cost", 0)
                        }
                    })
                
                # Upsert to Pinecone
                self.index.upsert(vectors=vectors_to_upsert)
                print(f"Indexed batch of {len(vectors_to_upsert)} vectors")
            
            except Exception as e:
                print(f"Error generating embeddings or indexing: {e}")
    
    def similarity_search(self, query: str, filter: Optional[Dict[str, Any]] = None, k: int = 3) -> List[Dict]:
        """Search for documents similar to the query using Pinecone."""
        try:
            # Generate embedding for query
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=[query]
            )
            query_embedding = response.data[0].embedding
            
            # Convert filter to Pinecone format if provided
            pinecone_filter = {}
            if filter:
                for key, value in filter.items():
                    pinecone_filter[key] = {"$eq": value}
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True,
                filter=pinecone_filter if pinecone_filter else None
            )
            
            # Format results to match our expected format
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "similarity": match.score,
                    "text": match.metadata.get("text", ""),
                    "metadata": {
                        "project_type": match.metadata.get("project_type", ""),
                        "square_feet": match.metadata.get("square_feet", 0),
                        "material_grade": match.metadata.get("material_grade", ""),
                        "total_cost": match.metadata.get("total_cost", 0)
                    }
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Error searching Pinecone: {e}")
            return []


# Factory function to get the appropriate vector store
def get_vector_store(use_mock=False, use_pinecone=False, data_file=None):
    """Get vector store instance based on configuration.
    
    Args:
        use_mock (bool): Force use of mock vector store
        use_pinecone (bool): Use Pinecone instead of in-memory store
        data_file (str, optional): Path to data file
        
    Returns:
        VectorStore: Mock, OpenAI, or Pinecone vector store instance
    """
    # Check environment variables
    mock_data = os.environ.get("MOCK_DATA", "true").lower() == "true"
    
    if use_mock or mock_data:
        print("Using MockVectorStore")
        return MockVectorStore(data_file)
    
    if use_pinecone or os.environ.get("USE_PINECONE", "false").lower() == "true":
        try:
            print("Using PineconeVectorStore")
            return PineconeVectorStore(data_file)
        except (ImportError, ValueError) as e:
            print(f"Error initializing PineconeVectorStore: {e}")
            print("Falling back to OpenAIVectorStore")
    
    try:
        print("Using OpenAIVectorStore")
        return OpenAIVectorStore(data_file)
    except (ImportError, ValueError) as e:
        print(f"Error initializing OpenAIVectorStore: {e}")
        print("Falling back to MockVectorStore")
        return MockVectorStore(data_file)
