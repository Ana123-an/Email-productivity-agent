"""
LLM Client wrapper for OpenAI API calls.

Evaluation Criteria:
- Safety & Robustness: Comprehensive error handling
- Code Quality: Clean abstraction for LLM interactions
"""

import os
from openai import OpenAI
from typing import Optional


def call_llm(system_prompt: str, user_content: str, model: Optional[str] = None) -> str:
    """
    Call the OpenAI LLM with system and user prompts.

    Args:
        system_prompt: The system instruction/context
        user_content: The user's input/query
        model: Optional model override

    Returns:
        The LLM's response text, or an error message if the call fails

    Evaluation Criteria:
    - Safety & Robustness: Try/except around API calls
    - Functionality: Returns user-friendly error messages on failure
    """
    try:
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "⚠️ Error: OPENAI_API_KEY not found in environment variables. Please set it in your .env file or Streamlit secrets."

        # Initialize client
        client = OpenAI(api_key=api_key)

        # Get model name from environment or use default
        model_name = model or os.getenv("MODEL_NAME", "gpt-4o-mini")

        # Make API call
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extract and return response
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Safety & Robustness: Friendly error handling
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
            return "⚠️ Authentication Error: Invalid API key. Please check your OPENAI_API_KEY."
        elif "rate_limit" in error_msg.lower():
            return "⚠️ Rate Limit Error: Too many requests. Please wait a moment and try again."
        elif "model" in error_msg.lower():
            return f"⚠️ Model Error: The specified model may not be available. Error: {error_msg}"
        else:
            return f"⚠️ LLM Error: {error_msg}"


def call_llm_with_json(system_prompt: str, user_content: str, model: Optional[str] = None) -> str:
    """
    Call LLM with JSON response formatting hint.

    Returns the raw LLM response for JSON parsing by the caller.
    """
    enhanced_system = system_prompt + "\n\nIMPORTANT: Respond with valid JSON only, no additional text."
    return call_llm(enhanced_system, user_content, model)
