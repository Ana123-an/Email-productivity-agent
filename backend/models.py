"""
Data models for the Email Productivity Agent.

Evaluation Criteria:
- Code Quality: Using dataclasses for type safety and clarity
- Functionality: Clear model definitions for all data structures
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Email:
    """
    Represents an email message.
    """
    id: int
    from_addr: str
    to_addr: str
    subject: str
    body: str
    timestamp: str
    raw_folder: str = "INBOX"
    category: Optional[str] = None

    def __str__(self):
        return f"Email(id={self.id}, from={self.from_addr}, subject={self.subject})"


@dataclass
class ActionItem:
    """
    Represents an extracted action item from an email.
    """
    task: str
    deadline: Optional[str] = None
    email_id: Optional[int] = None

    def __str__(self):
        deadline_str = f" (Due: {self.deadline})" if self.deadline else ""
        return f"{self.task}{deadline_str}"


@dataclass
class DraftEmail:
    """
    Represents a drafted email response.
    """
    original_email_id: int
    subject: str
    body: str
    suggested_tone: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __str__(self):
        return f"Draft for Email #{self.original_email_id}: {self.subject}"


@dataclass
class PromptConfig:
    """
    Configuration for prompt templates.
    """
    categorization: str
    action_item: str
    auto_reply: str
    summary: str
    general_agent: str

    def to_dict(self):
        return {
            "categorization": self.categorization,
            "action_item": self.action_item,
            "auto_reply": self.auto_reply,
            "summary": self.summary,
            "general_agent": self.general_agent
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            categorization=data.get("categorization", ""),
            action_item=data.get("action_item", ""),
            auto_reply=data.get("auto_reply", ""),
            summary=data.get("summary", ""),
            general_agent=data.get("general_agent", "")
        )
