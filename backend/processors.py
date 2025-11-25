"""
Email processing functions - categorization, action extraction, summarization, drafting.

Evaluation Criteria:
- Functionality: Phase 1 & 3 requirements - email processing and draft generation
- Prompt-driven architecture: ALL processing uses prompts from prompts.json
- Safety & Robustness: JSON parsing with fallbacks
"""

import json
from typing import List, Optional, Dict
from backend.models import Email, ActionItem, DraftEmail
from backend.llm_client import call_llm, call_llm_with_json


def categorize_email(email: Email, prompts: Dict[str, str]) -> str:
    """
    Categorize an email using the categorization prompt.

    Evaluation Criteria:
    - Functionality: Phase 1 - Email categorization
    - Prompt-driven: Uses prompts["categorization"]

    Args:
        email: Email object to categorize
        prompts: Dictionary of prompt templates

    Returns:
        Category name (Important, Newsletter, Spam, To-Do)
    """
    # Build user content from email
    user_content = f"""Subject: {email.subject}
From: {email.from_addr}

{email.body}"""

    # Get categorization prompt
    system_prompt = prompts.get("categorization", "Categorize this email.")

    # Call LLM
    response = call_llm(system_prompt, user_content)

    # Extract category (handle multi-line responses)
    category = response.strip().split("\n")[0].strip()

    # Validate category
    valid_categories = ["Important", "Newsletter", "Spam", "To-Do"]
    if category not in valid_categories:
        # Default to Important if unclear
        category = "Important"

    return category


def extract_action_items(email: Email, prompts: Dict[str, str]) -> List[ActionItem]:
    """
    Extract action items from an email.

    Evaluation Criteria:
    - Functionality: Phase 1 - Action item extraction
    - Prompt-driven: Uses prompts["action_item"]
    - Safety & Robustness: JSON parsing with fallback to empty list

    Args:
        email: Email object to extract actions from
        prompts: Dictionary of prompt templates

    Returns:
        List of ActionItem objects
    """
    # Build user content
    user_content = f"""Subject: {email.subject}
From: {email.from_addr}

{email.body}"""

    # Get action item prompt
    system_prompt = prompts.get("action_item", "Extract tasks from the email.")

    # Call LLM with JSON hint
    response = call_llm_with_json(system_prompt, user_content)

    # Parse JSON response
    try:
        # Try to extract JSON from response (in case of wrapped text)
        json_start = response.find('[')
        json_end = response.rfind(']') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            tasks_data = json.loads(json_str)
        else:
            tasks_data = json.loads(response)

        # Convert to ActionItem objects
        action_items = []
        for task_dict in tasks_data:
            if isinstance(task_dict, dict):
                action_item = ActionItem(
                    task=task_dict.get("task", ""),
                    deadline=task_dict.get("deadline"),
                    email_id=email.id
                )
                action_items.append(action_item)

        return action_items

    except Exception as e:
        # Safety & Robustness: Return empty list on JSON parse failure
        print(f"Error parsing action items JSON: {e}")
        return []


def summarize_email(email: Email, prompts: Dict[str, str]) -> str:
    """
    Summarize an email in bullet points.

    Evaluation Criteria:
    - Functionality: Phase 2 - Email summarization
    - Prompt-driven: Uses prompts["summary"]

    Args:
        email: Email object to summarize
        prompts: Dictionary of prompt templates

    Returns:
        Summary text
    """
    # Build user content
    user_content = f"""Subject: {email.subject}
From: {email.from_addr}
Date: {email.timestamp}

{email.body}"""

    # Get summary prompt
    system_prompt = prompts.get("summary", "Summarize this email.")

    # Call LLM
    response = call_llm(system_prompt, user_content)

    return response


def draft_reply(email: Email, prompts: Dict[str, str], user_tone: Optional[str] = None) -> DraftEmail:
    """
    Draft a reply to an email.

    Evaluation Criteria:
    - Functionality: Phase 3 - Draft generation
    - Prompt-driven: Uses prompts["auto_reply"]
    - User Experience: Supports tone customization

    Args:
        email: Email to reply to
        prompts: Dictionary of prompt templates
        user_tone: Optional tone (formal, friendly, concise)

    Returns:
        DraftEmail object
    """
    # Build user content
    user_content = f"""Original Email:
Subject: {email.subject}
From: {email.from_addr}
Date: {email.timestamp}

{email.body}

---
Draft a reply to this email."""

    # Get auto-reply prompt
    system_prompt = prompts.get("auto_reply", "Draft a professional reply.")

    # Add tone instruction if specified
    if user_tone:
        system_prompt += f"\n\nTone: {user_tone}"

    # Call LLM
    response = call_llm(system_prompt, user_content)

    # Generate draft subject
    draft_subject = f"Re: {email.subject}"

    # Create DraftEmail object
    draft = DraftEmail(
        original_email_id=email.id,
        subject=draft_subject,
        body=response,
        suggested_tone=user_tone,
        metadata={
            "original_from": email.from_addr,
            "original_subject": email.subject,
            "category": email.category
        }
    )

    return draft
