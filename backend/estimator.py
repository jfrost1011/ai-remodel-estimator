import os
import sys
from typing import Dict, Any, List, Optional
import json
import math
import random

# Import LangChain components
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_community.vectorstores import Pinecone as LangchainPinecone
import pinecone

# Import LangSmith for tracing
from langsmith import traceable

# Import our environment variable loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.env_loader import load_and_validate_env

# Import our vector store implementation
from backend.vector_store import PineconeVectorStore

# Import our LangSmith logger
from backend.langsmith_logger import get_langsmith_logger

# Initialize LangSmith logger
langsmith_logger = get_langsmith_logger()

class CostEstimator:
    """Cost estimator for renovation projects."""
    
    def __init__(self, vector_store=None):
        """Initialize with optional vector store."""
        # Load environment variables
        if not load_and_validate_env(["OPENAI_API_KEY"]):
            raise EnvironmentError("Failed to load required environment variables")
        
        # Initialize vector store
        if vector_store is None:
            try:
                # Try to use Pinecone vector store
                print("Initializing Pinecone vector store...")
                self.vector_store = PineconeVectorStore()
                print("Successfully initialized Pinecone vector store")
            except Exception as e:
                print(f"Error initializing Pinecone vector store: {e}")
                print("Falling back to mock vector store")
                from backend.vector_store import MockVectorStore
                self.vector_store = MockVectorStore()
        else:
            self.vector_store = vector_store
        
        # Initialize OpenAI client with GPT-4o-mini model
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini",
            temperature=0.1
        )
        
        # Initialize embeddings model
        self.embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
        
        # Create LangChain retriever if vector store is provided
        self.retriever = self._create_langchain_retriever()
        
        # Define prompt template for cost estimation
        self.prompt_template = ChatPromptTemplate.from_template("""
You are a renovation cost estimation expert. 

Given the following project details and reference projects, provide a detailed cost estimate.

Project Details:
- Project Type: {project_type}
- Square Footage: {square_feet}
- Material Grade: {material_grade}
- ZIP Code: {zip_code}
- Timeline (months): {timeline_months}

Reference Projects:
{reference_projects}

Please generate a cost estimate with the following:
1. Total cost range (min and max)
2. Timeline in weeks
3. Cost breakdown by category (materials, labor, permits, etc.)
4. Confidence level (0.0 to 1.0)

Format your response as a JSON object with the following structure:
{{
    "total_range": [min_cost, max_cost],
    "timeline_weeks": number_of_weeks,
    "confidence": confidence_score,
    "cost_breakdown": {{
        "materials": amount,
        "labor": amount,
        "permits": amount,
        "design": amount,
        "other": amount
    }}
}}

Include only the JSON object in your response, no other text.
""")
    
    def _create_langchain_retriever(self):
        """Create a LangChain retriever from our vector store."""
        # This method bridges our custom vector store with LangChain
        # by creating a retriever that LangChain can use
        
        class CustomRetriever:
            def __init__(self, vector_store):
                self.vector_store = vector_store
            
            def get_relevant_documents(self, query, **kwargs):
                # Use our vector store's similarity search
                results = self.vector_store.similarity_search(query, **kwargs)
                
                # Convert to LangChain Document objects
                documents = []
                for result in results:
                    content = result.get("text", "")
                    metadata = result.get("metadata", {})
                    documents.append(Document(page_content=content, metadata=metadata))
                
                return documents
                
        return CustomRetriever(self.vector_store)
    
    def estimate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a cost estimate based on input data."""
        # Use LangSmith logger's trace decorator if available
        if langsmith_logger.is_enabled():
            # Apply trace decorator dynamically
            traced_estimate = langsmith_logger.trace(
                name="cost_estimate", 
                run_type="chain"
            )(self._estimate)
            return traced_estimate(input_data)
        else:
            return self._estimate(input_data)
    
    def _estimate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to generate a cost estimate based on input data."""
        # Extract input parameters with support for both naming conventions
        project_type = input_data.get("project_type", input_data.get("room_type", "kitchen"))
        square_feet = input_data.get("square_feet", input_data.get("square_footage", 200))
        material_grade = input_data.get("material_grade", "standard")
        zip_code = input_data.get("zip_code", "00000")
        timeline_months = input_data.get("timeline_months", 2)
        
        # Retrieve similar projects
        query = f"{project_type} renovation with {square_feet} sq ft using {material_grade} materials"
        
        # Create a context for tracing vector search
        if langsmith_logger.is_enabled():
            search_context = langsmith_logger.create_run_context()
        else:
            # Create a dummy context if LangSmith is disabled
            class DummyContext:
                def __enter__(self): return self
                def __exit__(self, *args, **kwargs): pass
            search_context = DummyContext()
            
        # Perform vector search with tracing
        with search_context:
            # Get filter parameters
            filter_params = {
                "project_type": project_type,
                "material_grade": material_grade
            }
            
            # Perform vector search
            results = self.vector_store.similarity_search(query)
            
            # Convert to documents
            reference_docs = [Document(page_content=result["text"], metadata=result.get("metadata", {})) 
                               for result in results]
            reference_projects = "\n".join([doc.page_content for doc in reference_docs])
            
        # Create input for the LLM
        chain_input = {
            "project_type": project_type,
            "square_feet": square_feet,
            "material_grade": material_grade,
            "zip_code": zip_code,
            "timeline_months": timeline_months,
            "reference_projects": reference_projects
        }
        
        # Create and run the LangChain with tracing
        chain = self.prompt_template | self.llm
        
        # Create a context for tracing LLM call
        if langsmith_logger.is_enabled():
            llm_context = langsmith_logger.create_run_context()
        else:
            llm_context = DummyContext()
            
        # Make the LLM call with tracing
        with llm_context:
            try:
                # Make the LLM call
                result = chain.invoke(chain_input)
                
                # Extract content from LangChain's response format
                response_text = result.content
                
                # Parse the JSON response
                try:
                    estimate_data = json.loads(response_text)
                    return estimate_data
                except (json.JSONDecodeError, AttributeError) as e:
                    # Fallback to mock data if parsing fails
                    print(f"Error parsing LLM response: {e}")
                    return self._generate_mock_estimate(project_type, square_feet, material_grade)
                
            except Exception as e:
                print(f"Error during LLM call: {e}")
                return self._generate_mock_estimate(project_type, square_feet, material_grade)
    
    def _generate_mock_references(self, project_type: str, square_feet: int, material_grade: str) -> str:
        """Generate mock reference projects for testing."""
        # This is used only when vector store is not available
        base_costs = {
            "kitchen": {"standard": 250, "premium": 350, "luxury": 500},
            "bathroom": {"standard": 300, "premium": 450, "luxury": 650},
            "addition": {"standard": 350, "premium": 450, "luxury": 750}
        }
        
        base_cost = base_costs.get(project_type, {}).get(material_grade, 300)
        
        # Generate 3 similar mock projects
        projects = []
        for i in range(3):
            size_variance = random.uniform(0.85, 1.15)
            sample_size = int(square_feet * size_variance)
            sample_cost = int(base_cost * sample_size * random.uniform(0.9, 1.1))
            project = f"Project {i+1}: {project_type} renovation, {sample_size} sq ft, {material_grade} grade, total cost: ${sample_cost:,}"
            projects.append(project)
        
        return "\n".join(projects)
    
    def _generate_mock_estimate(self, project_type: str, square_feet: int, material_grade: str) -> Dict[str, Any]:
        """Generate a mock estimate when real data is unavailable."""
        # Base cost per square foot based on project type and material grade
        base_costs = {
            "kitchen": {"standard": 250, "premium": 350, "luxury": 500},
            "bathroom": {"standard": 300, "premium": 450, "luxury": 650},
            "addition": {"standard": 350, "premium": 450, "luxury": 750}
        }
        
        # Timeline in weeks
        timelines = {
            "kitchen": {"standard": 6, "premium": 8, "luxury": 10},
            "bathroom": {"standard": 4, "premium": 6, "luxury": 8},
            "addition": {"standard": 8, "premium": 12, "luxury": 16}
        }
        
        # Get base values
        base_cost = base_costs.get(project_type, {}).get(material_grade, 300)
        base_weeks = timelines.get(project_type, {}).get(material_grade, 8)
        
        # Calculate total cost range with variability
        mid_cost = base_cost * square_feet
        min_cost = int(mid_cost * 0.85)
        max_cost = int(mid_cost * 1.15)
        
        # Round to nearest thousand
        min_cost = math.floor(min_cost / 1000) * 1000
        max_cost = math.ceil(max_cost / 1000) * 1000
        
        # Cost breakdown
        materials_pct = {"standard": 0.4, "premium": 0.45, "luxury": 0.5}.get(material_grade, 0.4)
        labor_pct = {"standard": 0.35, "premium": 0.3, "luxury": 0.25}.get(material_grade, 0.35)
        
        mid_materials = int(mid_cost * materials_pct)
        mid_labor = int(mid_cost * labor_pct)
        mid_permits = int(mid_cost * 0.05)
        mid_design = int(mid_cost * 0.1)
        mid_other = mid_cost - mid_materials - mid_labor - mid_permits - mid_design
        
        # Final estimate
        estimate = {
            "total_range": [min_cost, max_cost],
            "timeline_weeks": base_weeks,
            "confidence": round(random.uniform(0.85, 0.95), 2),
            "cost_breakdown": {
                "materials": mid_materials,
                "labor": mid_labor,
                "permits": mid_permits,
                "design": mid_design,
                "other": mid_other
            }
        }
        
        return estimate

# Simple test function to demonstrate usage
def test_estimator():
    """Test the estimator with a sample query."""
    estimator = CostEstimator()
    
    # Test LLM
    query = "What's a good cost range for a 200 sqft kitchen remodel?"
    response = estimator.estimate({"project_type": "kitchen", "square_feet": 200})
    print(f"Query: {query}")
    print(f"Response: {response}")
    
    # Test embeddings
    text = "Kitchen remodel with granite countertops"
    embedding = estimator.embeddings.embed_query(text)
    print(f"Generated embedding with {len(embedding)} dimensions")
    print(f"First 5 values: {embedding[:5]}")

if __name__ == "__main__":
    test_estimator()
