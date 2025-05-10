"""
LangSmith integration for tracing and monitoring LLM operations.

This module provides a simple interface for integrating LangSmith into the renovation estimator project.
It enables tracing of AI operations and recording feedback for evaluation and improvement.

Usage:
    # Import the logger
    from backend.langsmith_logger import get_langsmith_logger
    
    # Get a singleton instance
    langsmith_logger = get_langsmith_logger()
    
    # Check if LangSmith is enabled
    if langsmith_logger.is_enabled():
        # Apply traceable decorator to a function
        @langsmith_logger.trace(name="my_function", run_type="chain")
        def my_function(input_data):
            # Function implementation
            return result
            
    # Record feedback
    langsmith_logger.record_feedback(
        run_id="run-id-from-langsmith",
        key="accuracy",
        score=0.95,
        comment="Very accurate estimate"
    )

For more information, see docs/langsmith_integration.md
"""
import os
import sys
from typing import Dict, Any, Optional, List, Callable, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our environment variable loader
from utils.env_loader import load_env_vars

# Import LangSmith components with proper error handling
try:
    from langsmith import Client, traceable
    from langchain.callbacks.tracers.langchain import wait_for_all_tracers
    from langchain.callbacks.tracers import LangChainTracer
    
    # Try importing tracing_enabled from different modules (handle API changes)
    try:
        from langchain.callbacks.tracers.langchain import tracing_enabled
    except ImportError:
        try:
            from langchain_core.tracers.langchain import tracing_enabled
        except ImportError:
            # Define a fallback if import fails
            def tracing_enabled(project_name=None):
                class DummyTracer:
                    def __enter__(self): return self
                    def __exit__(self, *args, **kwargs): pass
                return DummyTracer()
    
    LANGSMITH_AVAILABLE = True
except ImportError:
    # Define placeholder components if LangSmith is not available
    LANGSMITH_AVAILABLE = False
    
    # Create stub for traceable decorator
    def traceable(name="run", run_type="chain"):
        def decorator(func):
            return func
        return decorator
    
    # Create stubs for other missing classes/functions
    class LangChainTracer:
        pass
    
    def wait_for_all_tracers():
        pass
    
    def tracing_enabled(project_name=None):
        class DummyTracer:
            def __enter__(self): return self
            def __exit__(self, *args, **kwargs): pass
        return DummyTracer()
    
    # Log the import error
    logger.warning("LangSmith not available. Install with 'pip install langsmith'")

class LangSmithLogger:
    """
    A streamlined logger for LangSmith integration to track LLM operations.
    """
    
    def __init__(self, project_name: str = "renovation-estimator"):
        """
        Initialize the LangSmith logger.
        
        Args:
            project_name: The name of the project in LangSmith
        """
        self.project_name = project_name
        self.client = None
        self.enabled = False
        
        # Try to load environment variables if not already loaded
        load_env_vars()
        
        # Try to initialize LangSmith client
        self.api_key = os.environ.get("LANGSMITH_API_KEY")
        
        if LANGSMITH_AVAILABLE and self.api_key:
            try:
                self.client = Client(api_key=self.api_key)
                self.enabled = True
                logger.info(f"LangSmith logger initialized for project: {project_name}")
                
                # Set environment variables for LangChain tracing
                os.environ["LANGCHAIN_TRACING_V2"] = "true"
                os.environ["LANGCHAIN_PROJECT"] = project_name
            except Exception as e:
                logger.error(f"Failed to initialize LangSmith client: {e}")
        else:
            logger.warning("LangSmith integration is disabled (API key not found or module not available)")
    
    def is_enabled(self) -> bool:
        """Check if LangSmith logging is enabled."""
        return self.enabled and LANGSMITH_AVAILABLE
    
    def trace(self, name: str = "run", run_type: str = "chain") -> Callable:
        """
        Get a decorator to trace a function with LangSmith.
        
        This is a more intuitive name for the traceable decorator.
        
        Args:
            name: The name of the run
            run_type: The type of run (e.g., "chain", "llm", "tool")
            
        Returns:
            A decorator function or a no-op decorator if LangSmith is disabled
        """
        if not self.is_enabled():
            # Return a no-op decorator if LangSmith is disabled
            return lambda func: func
        
        # Return the traceable decorator from LangSmith
        return traceable(name=name, run_type=run_type)
    
    def create_run_context(self, tags: List[str] = None):
        """
        Create a context manager for tracing a block of code.
        
        Args:
            tags: Optional list of tags to apply to the run
            
        Returns:
            A context manager for tracing
        """
        if not self.is_enabled():
            # Return a dummy context manager if LangSmith is disabled
            class DummyContext:
                def __enter__(self): return self
                def __exit__(self, *args, **kwargs): pass
            return DummyContext()
        
        # Return a real tracing context
        return tracing_enabled(project_name=self.project_name)
    
    def record_feedback(self, run_id: str, key: str, score: float, comment: Optional[str] = None) -> bool:
        """
        Record feedback for a run.
        
        Args:
            run_id: The ID of the run
            key: The type of feedback (e.g., "accuracy", "helpfulness")
            score: The score (typically between 0 and 1)
            comment: An optional comment
            
        Returns:
            True if feedback was recorded successfully, False otherwise
        """
        if not self.is_enabled() or not run_id:
            return False
        
        try:
            self.client.create_feedback(
                run_id=run_id,
                key=key,
                score=score,
                comment=comment
            )
            return True
        except Exception as e:
            logger.error(f"Failed to record feedback: {e}")
            return False
    
    def wait_for_tracers(self):
        """Wait for all pending tracers to complete."""
        if self.is_enabled():
            wait_for_all_tracers()

# Singleton instance
_INSTANCE = None

def get_langsmith_logger(project_name: str = None) -> LangSmithLogger:
    """
    Get a singleton instance of the LangSmith logger.
    
    Args:
        project_name: Optional project name override
        
    Returns:
        LangSmithLogger: An instance of the LangSmith logger
    """
    global _INSTANCE
    
    # Get project name from environment if not provided
    if project_name is None:
        project_name = os.environ.get("LANGSMITH_PROJECT", "renovation-estimator")
    
    # Create instance if it doesn't exist
    if _INSTANCE is None:
        _INSTANCE = LangSmithLogger(project_name)
    
    return _INSTANCE

def test_langsmith_logger():
    """Test the LangSmith logger."""
    ls_logger = get_langsmith_logger()
    
    print(f"LangSmith logging enabled: {ls_logger.is_enabled()}")
    
    if not ls_logger.is_enabled():
        print("LangSmith API key not found or module not available. Skipping test.")
        return
    
    # Define a sample function to trace
    @ls_logger.trace(name="test_function", run_type="chain")
    def sample_function(x, y):
        return x + y
    
    # Call the traced function
    result = sample_function(3, 4)
    print(f"Sample function result: {result}")
    
    # Use the context manager
    with ls_logger.create_run_context(tags=["test"]):
        print("Running code in traced context")
    
    # Wait for tracers to complete
    ls_logger.wait_for_tracers()
    
    print("Check your LangSmith dashboard for the trace.")

if __name__ == "__main__":
    test_langsmith_logger() 