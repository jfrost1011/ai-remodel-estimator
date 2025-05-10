"""
Environment variable loader utilities.

This module provides functions to safely load environment variables with fallbacks.
"""

import os
from typing import Any, Optional

def load_env_var(key: str, default: Optional[Any] = None) -> Any:
    """
    Load an environment variable with a fallback default value.
    
    Args:
        key: The environment variable key to load
        default: Default value to return if the key is not found
        
    Returns:
        The value of the environment variable or the default
    """
    return os.environ.get(key, default) 