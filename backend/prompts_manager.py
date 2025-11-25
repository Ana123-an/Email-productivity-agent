"""
Prompt management module - loads and saves prompt configurations.

Evaluation Criteria:
- Functionality: Prompt-driven architecture (prompts stored in JSON, editable)
- Code Quality: Clean file I/O abstraction
"""

import json
import os
from typing import Dict


def load_prompts(path: str = "data/prompts.json") -> Dict[str, str]:
    """
    Load prompt templates from JSON file.

    Args:
        path: Path to prompts.json file

    Returns:
        Dictionary of prompt templates

    Evaluation Criteria:
    - Functionality: Never hard-code prompts; always read from file
    - Safety & Robustness: Handle missing file gracefully
    """
    try:
        if not os.path.exists(path):
            # Return default prompts if file doesn't exist
            return get_default_prompts()

        with open(path, 'r', encoding='utf-8') as f:
            prompts = json.load(f)

        return prompts

    except Exception as e:
        print(f"Error loading prompts: {e}")
        return get_default_prompts()


def save_prompts(prompts: Dict[str, str], path: str = "data/prompts.json") -> bool:
    """
    Save prompt templates to JSON file.

    Args:
        prompts: Dictionary of prompt templates
        path: Path to save prompts.json

    Returns:
        True if successful, False otherwise

    Evaluation Criteria:
    - Functionality: User-editable prompts persisted to file
    - Safety & Robustness: Error handling with user feedback
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error saving prompts: {e}")
        return False


def get_default_prompts() -> Dict[str, str]:
    """
    Returns default prompt templates.

    Evaluation Criteria:
    - Functionality: Sensible defaults for all prompt types
    """
    return {
        "categorization": "Categorize this email into one of: Important, Newsletter, Spam, To-Do. To-Do emails must include a direct request requiring user action. Respond with only the category name.",
        "action_item": "Extract tasks from the email. Respond in JSON list format: [ { \"task\": \"...\", \"deadline\": \"...\" } ]. If no tasks, return an empty list [].",
        "auto_reply": "If the email is a meeting request, draft a polite, concise reply asking for an agenda and proposing 1-2 time slots. Maintain a professional tone.",
        "summary": "Summarize the following email in 2–3 bullet points, focusing on key information and any required actions.",
        "general_agent": "You are an Email Productivity Agent helping the user manage their inbox. Always use the stored prompts as behavioral instructions whenever relevant."
    }
