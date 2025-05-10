"""
Backend package for the Renovation Cost Estimator.

This package contains the business logic and data processing components.
"""

# Import main modules to make them available at package level
from renovation_estimator.backend.estimator import get_cost_estimate
from renovation_estimator.backend.vector_store import search_similar_projects

__all__ = ['get_cost_estimate', 'search_similar_projects'] 