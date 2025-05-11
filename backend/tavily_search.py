"""
Tavily Search Module for Renovation Cost Estimator

This module provides search capabilities using the Tavily API to find up-to-date
renovation cost information from the web. It enhances the accuracy of cost estimates
by providing real-time market data for different locations and project types.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Set up logging
logger = logging.getLogger(__name__)

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    logger.warning("Tavily package not installed. Real-time cost searches will be unavailable.")
    TAVILY_AVAILABLE = False

class TavilySearchProvider:
    """Class for performing searches using the Tavily API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tavily search provider.
        
        Args:
            api_key: Tavily API key (optional, will use environment variable if not provided)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.client = None
        
        if self.api_key and TAVILY_AVAILABLE:
            try:
                self.client = TavilyClient(api_key=self.api_key)
                logger.info("Tavily client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Tavily client: {str(e)}")
    
    @property
    def is_available(self) -> bool:
        """Check if Tavily search is available."""
        return TAVILY_AVAILABLE and self.client is not None
    
    def search(self, query: str, search_depth: str = "advanced") -> Optional[Dict[str, Any]]:
        """
        Perform a search using the Tavily API.
        
        Args:
            query: The search query string
            search_depth: The depth of search ('basic' or 'advanced')
            
        Returns:
            The search results from Tavily or None if search fails
        """
        if not self.is_available:
            logger.warning("Tavily search is not available. Check API key and package installation.")
            return None
        
        try:
            logger.info(f"Performing Tavily search with query: {query}")
            response = self.client.search(query, search_depth=search_depth)
            return response
        except Exception as e:
            logger.error(f"Error performing Tavily search: {str(e)}")
            return None
    
    def get_renovation_costs(self, 
                           project_type: str, 
                           location: str, 
                           extra_context: str = "") -> Tuple[Dict[str, Any], List[str]]:
        """
        Get renovation costs for a specific project type and location.
        
        Args:
            project_type: Type of renovation (kitchen, bathroom, etc.)
            location: Location (city, state, zip code)
            extra_context: Additional context for the search
            
        Returns:
            Tuple containing (all results, list of extracted cost ranges)
        """
        # Construct search query
        query = f"current {project_type} renovation cost in {location} {extra_context}"
        
        # Perform search
        results = self.search(query)
        
        # Extract cost information
        cost_ranges = []
        if results and "results" in results:
            for result in results["results"]:
                content = result.get("content", "")
                cost_ranges.extend(self.extract_cost_ranges(content))
        
        return results, cost_ranges
    
    @staticmethod
    def extract_cost_ranges(text: str) -> List[str]:
        """
        Extract cost ranges from text using regex.
        
        Args:
            text: The text to search for cost ranges
            
        Returns:
            List of found cost ranges
        """
        # Pattern for finding dollar amounts, including ranges
        # Matches patterns like $30,000, $30k, $30,000 to $90,000, $30,000-$90,000
        pattern = r'\$\s*[\d,]+(?:\.\d+)?(?:\s*[kK])?(?:\s*(?:to|-)\s*\$\s*[\d,]+(?:\.\d+)?(?:\s*[kK])?)?'
        
        # Find all matches
        matches = re.findall(pattern, text)
        
        return matches
    
    def get_cost_summary(self, 
                        project_type: str, 
                        location: str,
                        size: Optional[int] = None,
                        quality: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a summary of costs for a renovation project.
        
        Args:
            project_type: Type of renovation (kitchen, bathroom, etc.)
            location: Location (city, state, zip code)
            size: Size of the project in square feet (optional)
            quality: Quality level (economy, standard, premium, luxury) (optional)
            
        Returns:
            Dictionary with cost summary information
        """
        # Construct extra context from size and quality if provided
        extra_context = ""
        if size:
            extra_context += f" {size} square feet"
        if quality:
            extra_context += f" {quality} quality"
        
        # Get results and cost ranges
        results, cost_ranges = self.get_renovation_costs(project_type, location, extra_context)
        
        # Prepare summary
        summary = {
            "query": f"{project_type} renovation in {location}{extra_context}",
            "cost_ranges": cost_ranges[:10],  # Limit to first 10 ranges
            "found_costs": len(cost_ranges) > 0,
            "source_count": len(results.get("results", [])) if results else 0,
            "top_sources": []
        }
        
        # Add top sources
        if results and "results" in results:
            for result in results["results"][:3]:  # Top 3 sources
                source = {
                    "title": result.get("title", "Untitled"),
                    "url": result.get("url", ""),
                    "preview": result.get("content", "")[:200].replace("\n", " ").strip()
                }
                summary["top_sources"].append(source)
        
        return summary

# Singleton instance for reuse
_tavily_provider = None

def get_tavily_provider() -> TavilySearchProvider:
    """Get the singleton instance of the Tavily search provider."""
    global _tavily_provider
    if _tavily_provider is None:
        _tavily_provider = TavilySearchProvider()
    return _tavily_provider

def search_renovation_costs(project_type: str, location: str, size: Optional[int] = None, 
                           quality: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for renovation costs using Tavily.
    
    Args:
        project_type: Type of renovation (kitchen, bathroom, etc.)
        location: Location (city, state, zip code)
        size: Size of the project in square feet (optional)
        quality: Quality level (economy, standard, premium, luxury) (optional)
        
    Returns:
        Dictionary with cost summary information
    """
    provider = get_tavily_provider()
    if not provider.is_available:
        return {
            "error": "Tavily search is not available. Please check API key and package installation.",
            "found_costs": False,
            "cost_ranges": [],
            "top_sources": []
        }
    
    return provider.get_cost_summary(project_type, location, size, quality) 