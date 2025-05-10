import json
import os
import numpy as np
import sys
import pinecone
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec

# Import LangChain components
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our environment variable loader and data loader
from utils.env_loader import load_env_vars
from utils.data_loader import load_project_data, format_data_for_vector_store, save_project_data

class MockVectorStore:
    """Simulated vector store for rapid development."""
    
    def __init__(self, data_file=None):
        """Initialize with synthetic data."""
        # Use the centralized data loader utility
        self.data = load_project_data(
            data_file=data_file,
            fallback_to_synthetic=True,
            count=50,
            return_formatted=True
        )
        
        if self.data:
            print(f"MockVectorStore initialized with {len(self.data)} projects")
        else:
            print("Warning: MockVectorStore initialized with empty dataset")
    
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
        
        # Use the centralized data loader utility
        self.data = load_project_data(
            data_file=data_file,
            fallback_to_synthetic=True,
            count=20,
            return_formatted=True
        )
        
        if self.data:
            print(f"OpenAIVectorStore initialized with {len(self.data)} projects")
        else:
            print("Warning: OpenAIVectorStore initialized with empty dataset")
            
        # Generate embeddings if not already present
        self._ensure_embeddings()
    
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
        # Use the centralized data saving utility
        save_data = []
        for doc in self.data:
            doc_copy = doc.copy()
            if "embedding" in doc_copy:
                # Convert numpy arrays to lists for JSON serialization
                if isinstance(doc_copy["embedding"], np.ndarray):
                    doc_copy["embedding"] = doc_copy["embedding"].tolist()
            save_data.append(doc_copy)
        
        save_project_data(save_data, "data/embeddings/embedded_projects.json")
    
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
    """
    Vector store implementation using Pinecone for similarity search.
    """
    
    def __init__(self):
        """Initialize the Pinecone vector store."""
        # Load environment variables
        if not load_env_vars():
            raise EnvironmentError("Failed to load required environment variables")
        
        # Get Pinecone configuration from environment variables
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.index_name = os.getenv("PINECONE_INDEX", "renovation-estimator")
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        # Initialize Pinecone with the new API
        self.pc = Pinecone(api_key=self.api_key)
        
        # Check if index exists, create if it doesn't
        existing_indexes = self.pc.list_indexes()
        index_names = [index.name for index in existing_indexes]
        
        if self.index_name not in index_names:
            print(f"Creating Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embeddings dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=self.environment
                )
            )
        
        # Connect to the index
        self.index = self.pc.Index(self.index_name)
        print(f"Connected to Pinecone index: {self.index_name}")
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Add texts to the vector store.
        
        Args:
            texts: List of text strings to add
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            List of IDs for the added texts
        """
        from langchain_openai import OpenAIEmbeddings
        
        # Initialize embeddings model
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
        
        # Generate embeddings for texts
        vectors = embeddings.embed_documents(texts)
        
        # Generate IDs if not provided
        ids = [f"text_{i}" for i in range(len(texts))]
        
        # Prepare vectors for upsert
        vectors_to_upsert = []
        for i, (text, vector) in enumerate(zip(texts, vectors)):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            metadata["text"] = text  # Store the original text in metadata
            vectors_to_upsert.append({
                "id": ids[i],
                "values": vector,
                "metadata": metadata
            })
        
        # Upsert vectors to Pinecone
        self.index.upsert(vectors=vectors_to_upsert)
        
        return ids
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar texts using the query string.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of dictionaries containing text and metadata
        """
        from langchain_openai import OpenAIEmbeddings
        
        # Initialize embeddings model
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
        
        # Generate embedding for query
        query_embedding = embeddings.embed_query(query)
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        # Format results
        formatted_results = []
        for match in results.matches:
            formatted_results.append({
                "id": match.id,
                "score": match.score,
                "text": match.metadata.get("text", ""),
                "metadata": {k: v for k, v in match.metadata.items() if k != "text"}
            })
        
        return formatted_results
    
    def delete(self, ids: List[str]) -> None:
        """
        Delete vectors by ID.
        
        Args:
            ids: List of IDs to delete
        """
        self.index.delete(ids=ids)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary of index statistics
        """
        return self.index.describe_index_stats()


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
            return PineconeVectorStore()
        except (ImportError, ValueError) as e:
            print(f"Error initializing PineconeVectorStore: {e}")
            print("Falling back to OpenAIVectorStore")
            return OpenAIVectorStore(data_file)
    
    # Default to OpenAI vector store
    print("Using OpenAIVectorStore")
    return OpenAIVectorStore(data_file)
