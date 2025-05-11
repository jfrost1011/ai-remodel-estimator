"""
UI Components for Renovation Cost Estimator

This package contains the UI components for the Renovation Cost Estimator application.
"""

# Import market research component for easy access
try:
    from .market_research_component import (
        render_market_research_section,
        market_research_page,
        display_market_research_results
    )
except ImportError:
    # Fallback to prevent errors if the module isn't available
    pass 