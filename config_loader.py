import yaml
import streamlit as st
from typing import Dict, Any
import os
from pathlib import Path

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.yaml and combine with Streamlit secrets.
    
    Returns:
        Dict[str, Any]: Complete configuration dictionary
    """
    # Load YAML config
    config_path = Path(__file__).parent / "config" / "config.yaml"
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"Configuration file not found: {config_path}")
        config = {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing configuration file: {e}")
        config = {}
    
    return config

def get_llm_config() -> Dict[str, Any]:
    """
    Get LLM configuration with API credentials from Streamlit secrets.
    
    Returns:
        Dict[str, Any]: LLM configuration ready for CustomLLM class
    """
    config = load_config()
    llm_config = config.get("llm", {})
    
    # Build headers with API key from secrets
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    except KeyError:
        st.error("OpenAI API key not found in secrets. Please add OPENAI_API_KEY to .streamlit/secrets.toml")
        headers = {}
    
    # Build complete LLM config
    llm_interface_config = {
        "chat_endpoint": llm_config.get("endpoints", {}).get("chat", "https://api.openai.com/v1/chat/completions"),
        "embedding_endpoint": llm_config.get("endpoints", {}).get("embedding", "https://api.openai.com/v1/embeddings"),
        "headers": headers,
        "default_model": llm_config.get("default_model", "gpt-4"),
        "temperature": llm_config.get("temperature", 0.3),
        "max_retries": llm_config.get("max_retries", 3),
        "retry_delay": llm_config.get("retry_delay", 1)
    }
    
    return llm_interface_config

def get_app_config() -> Dict[str, Any]:
    """
    Get application configuration settings.
    
    Returns:
        Dict[str, Any]: Application configuration
    """
    config = load_config()
    return config.get("app", {})

def get_job_templates() -> Dict[str, str]:
    """
    Get job description templates from configuration.
    
    Returns:
        Dict[str, str]: Job templates mapping
    """
    config = load_config()
    return config.get("job_templates", {})
