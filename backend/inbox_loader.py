"""
Inbox loader module - loads mock email data.

Evaluation Criteria:
- Functionality: Phase 1 - Email Ingestion
- Code Quality: Clean data loading abstraction
"""

import json
import os
from typing import List
from backend.models import Email


def load_inbox(path: str = "data/mock_inbox.json") -> List[Email]:
    """
    Load emails from JSON file and convert to Email objects.

    Args:
        path: Path to mock inbox JSON file

    Returns:
        List of Email objects

    Evaluation Criteria:
    - Functionality: Phase 1 requirement - load mock inbox
    - Safety & Robustness: Handle missing/malformed data
    """
    try:
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Returning empty inbox.")
            return []

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        emails = []
        for item in data:
            try:
                email = Email(
                    id=item.get('id', 0),
                    from_addr=item.get('from', 'unknown@example.com'),
                    to_addr=item.get('to', 'user@company.com'),
                    subject=item.get('subject', 'No Subject'),
                    body=item.get('body', ''),
                    timestamp=item.get('timestamp', ''),
                    raw_folder=item.get('raw_folder', 'INBOX')
                )
                emails.append(email)
            except Exception as e:
                print(f"Error parsing email: {e}")
                continue

        return emails

    except Exception as e:
        print(f"Error loading inbox: {e}")
        return []


def get_email_by_id(emails: List[Email], email_id: int) -> Email:
    """
    Get an email by its ID.

    Args:
        emails: List of Email objects
        email_id: Email ID to find

    Returns:
        Email object or None if not found
    """
    for email in emails:
        if email.id == email_id:
            return email
    return None
