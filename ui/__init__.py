"""
UI package for the Renovation Cost Estimator.

This package contains Streamlit UI components and page definitions.
"""

# Import main page renderers to make them available at package level
from renovation_estimator.ui.home_page import render_home_page
from renovation_estimator.ui.estimate_page import render_estimate_page
from renovation_estimator.ui.search_page import render_search_page
from renovation_estimator.ui.dashboard_page import render_dashboard_page
from renovation_estimator.ui.admin_page import render_admin_page

__all__ = [
    'render_home_page', 
    'render_estimate_page', 
    'render_search_page', 
    'render_dashboard_page', 
    'render_admin_page'
] 