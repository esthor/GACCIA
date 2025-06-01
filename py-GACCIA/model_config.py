"""
Model Configuration Utilities for GACCIA

This module provides utilities for creating models with support for both 
OpenAI and Koyeb-hosted endpoints.
"""

import os
from typing import Optional, Union

from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike


def create_model(
    model_id: str = "gpt-4.1", 
    use_koyeb: bool = False,
    api_key: Optional[str] = None
) -> Union[OpenAIChat, OpenAILike]:
    """
    Create a model instance that can use either OpenAI or Koyeb endpoints.
    
    Args:
        model_id: The model ID to use (e.g., "gpt-4.1", "gpt-4o")
        use_koyeb: Whether to use Koyeb-hosted models instead of OpenAI
        api_key: Optional API key override. If not provided, uses environment variables.
    
    Returns:
        Model instance configured for the specified endpoint
    """
    if use_koyeb:
        # Use Koyeb-hosted OpenAI-compatible endpoint
        base_url = os.getenv("KOYEB_OPENAI_LIKE_BASE_URL")
        if not base_url:
            raise ValueError("KOYEB_OPENAI_LIKE_BASE_URL environment variable is required when use_koyeb=True")
        
        # For Koyeb, we might use a different API key or "null" as shown in examples
        koyeb_api_key = api_key or os.getenv("KOYEB_API_KEY", "null")
        
        return OpenAILike(
            id=model_id,
            api_key=koyeb_api_key,
            base_url=base_url,
        )
    else:
        # Use standard OpenAI endpoint
        openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required when use_koyeb=False")
        
        return OpenAIChat(
            id=model_id,
            api_key=openai_api_key
        )


def get_model_config_info(use_koyeb: bool = False) -> str:
    """Get information about the current model configuration."""
    if use_koyeb:
        base_url = os.getenv("KOYEB_OPENAI_LIKE_BASE_URL", "Not configured")
        return f"Using Koyeb endpoint: {base_url}"
    else:
        return "Using OpenAI endpoint: https://api.openai.com/v1"
