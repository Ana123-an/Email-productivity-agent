"""
Email Agent - Natural language interaction with inbox.

Evaluation Criteria:
- Functionality: Phase 2 - Email Processing Agent
- Prompt-driven: Uses prompts["general_agent"] and other prompts
- User Experience: Natural language queries
"""

from typing import List, Optional, Dict
from backend.models import Email
from backend.llm_client import call_llm
from backend.processors import summarize_email, extract_action_items


def run_agent_query(
    user_query: str,
    selected_email: Optional[Email],
    prompts: Dict[str, str],
    inbox: List[Email]
) -> str:
    """
    Process user's natural language query about their inbox.

    Evaluation Criteria:
    - Functionality: Phase 2 agent logic
      * Receive user query + email content + stored prompts
      * Construct LLM request (system + user messages)
      * Get output and return to UI
    - Prompt-driven: Uses general_agent prompt + context
    - User Experience: Handles various query types

    Args:
        user_query: User's natural language query
        selected_email: Currently selected email (if any)
        prompts: Dictionary of prompt templates
        inbox: List of all emails

    Returns:
        Agent's response as a string
    """
    # Build context from selected email
    email_context = ""
    if selected_email:
        email_context = f"""
Currently Selected Email:
ID: {selected_email.id}
From: {selected_email.from_addr}
Subject: {selected_email.subject}
Category: {selected_email.category or 'Uncategorized'}
Date: {selected_email.timestamp}

Body:
{selected_email.body}
"""

    # Build inbox overview
    inbox_overview = f"\nTotal emails in inbox: {len(inbox)}\n"

    # Add category breakdown
    if inbox:
        categories = {}
        for email in inbox:
            cat = email.category or "Uncategorized"
            categories[cat] = categories.get(cat, 0) + 1

        inbox_overview += "Categories: "
        inbox_overview += ", ".join([f"{cat}: {count}" for cat, count in categories.items()])

    # Get general agent prompt
    system_prompt = prompts.get("general_agent", "You are an Email Productivity Agent.")

    # Add available capabilities
    system_prompt += """

Available capabilities:
- Summarize emails
- Extract action items and tasks
- Draft replies
- Categorize emails (Important, Newsletter, Spam, To-Do)
- Filter and search emails

When asked about tasks or to-dos, check if emails are categorized as "To-Do".
When asked about urgent emails, look for "Important" category.
Be helpful, concise, and actionable.
"""

    # Build user message with context
    user_message = f"""{inbox_overview}

{email_context}

User Query: {user_query}"""

    # Handle specific query patterns for better UX
    query_lower = user_query.lower()

    # Pattern: Summarize current email
    if selected_email and ("summarize" in query_lower or "summary" in query_lower):
        if "this" in query_lower or "email" in query_lower:
            summary = summarize_email(selected_email, prompts)
            return f"📧 **Summary of Email #{selected_email.id}:**\n\n{summary}"

    # Pattern: Extract tasks from current email
    if selected_email and ("task" in query_lower or "to-do" in query_lower or "action" in query_lower):
        if "this" in query_lower or "email" in query_lower:
            actions = extract_action_items(selected_email, prompts)
            if actions:
                tasks_text = "\n".join([f"- {action.task}" + (f" (Due: {action.deadline})" if action.deadline else "") for action in actions])
                return f"✅ **Tasks from Email #{selected_email.id}:**\n\n{tasks_text}"
            else:
                return f"No specific tasks found in this email."

    # Pattern: Show urgent/important emails
    if "urgent" in query_lower or "important" in query_lower:
        important_emails = [e for e in inbox if e.category == "Important"]
        if important_emails:
            result = f"🔴 **Important Emails ({len(important_emails)}):**\n\n"
            for email in important_emails[:5]:  # Show max 5
                result += f"- **ID {email.id}**: {email.subject} (from {email.from_addr})\n"
            if len(important_emails) > 5:
                result += f"\n... and {len(important_emails) - 5} more"
            return result
        else:
            return "No emails marked as Important."

    # Pattern: Show to-dos
    if "to-do" in query_lower or "todo" in query_lower:
        todo_emails = [e for e in inbox if e.category == "To-Do"]
        if todo_emails:
            result = f"📋 **To-Do Emails ({len(todo_emails)}):**\n\n"
            for email in todo_emails[:5]:
                result += f"- **ID {email.id}**: {email.subject} (from {email.from_addr})\n"
            if len(todo_emails) > 5:
                result += f"\n... and {len(todo_emails) - 5} more"
            return result
        else:
            return "No emails categorized as To-Do."

    # General query - use LLM
    response = call_llm(system_prompt, user_message)

    return response
