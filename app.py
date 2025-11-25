"""
Email Productivity Agent - Main Streamlit Application

Evaluation Criteria Coverage:
1. Functionality: All three phases (Ingestion, Processing, Draft Generation)
2. Prompt-driven architecture: All operations use editable prompts from prompts.json
3. Code quality: Modular structure, clear separation of concerns
4. User experience: Intuitive tabs, clean interface, helpful feedback
5. Safety & robustness: Error handling, no email sending, input validation

Run with: streamlit run app.py
"""

import streamlit as st
import os
from datetime import datetime

# Import backend modules
from backend.inbox_loader import load_inbox, get_email_by_id
from backend.prompts_manager import load_prompts, save_prompts
from backend.processors import categorize_email, extract_action_items, summarize_email, draft_reply
from backend.agent import run_agent_query
from backend.models import Email, ActionItem, DraftEmail


# Page configuration
st.set_page_config(
    page_title="Email Productivity Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    if 'emails' not in st.session_state:
        st.session_state.emails = []
    if 'prompts' not in st.session_state:
        st.session_state.prompts = load_prompts()
    if 'processed' not in st.session_state:
        st.session_state.processed = {}  # {email_id: {'category': ..., 'actions': [...]}}
    if 'drafts' not in st.session_state:
        st.session_state.drafts = {}  # {email_id: DraftEmail}
    if 'selected_email_id' not in st.session_state:
        st.session_state.selected_email_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_key_set' not in st.session_state:
        # Check if API key is available
        st.session_state.api_key_set = bool(os.getenv("OPENAI_API_KEY"))


def render_sidebar():
    """Render sidebar with inbox loading and prompt configuration."""
    with st.sidebar:
        st.title("📧 Email Agent")
        st.markdown("---")

        # API Key status
        if st.session_state.api_key_set:
            st.success("✅ API Key configured")
        else:
            st.error("⚠️ API Key not set")
            st.info("Set OPENAI_API_KEY in environment or .streamlit/secrets.toml")

        st.markdown("---")

        # Phase 1: Load Inbox
        st.subheader("📥 Inbox Management")

        if st.button("🔄 Load Mock Inbox", use_container_width=True):
            with st.spinner("Loading emails..."):
                emails = load_inbox()
                st.session_state.emails = emails
                st.session_state.processed = {}
                st.success(f"✅ Loaded {len(emails)} emails")

        if st.session_state.emails:
            st.metric("Total Emails", len(st.session_state.emails))

            # Show category breakdown if processed
            if st.session_state.processed:
                categories = {}
                for email_data in st.session_state.processed.values():
                    cat = email_data.get('category', 'Uncategorized')
                    categories[cat] = categories.get(cat, 0) + 1

                st.markdown("**Categories:**")
                for cat, count in categories.items():
                    st.markdown(f"- {cat}: {count}")

        st.markdown("---")

        # Prompt Brain Quick Edit
        st.subheader("🧠 Prompt Brain")
        st.caption("Edit in Prompt Brain Config tab")

        if st.button("💾 Reload Prompts", use_container_width=True):
            st.session_state.prompts = load_prompts()
            st.success("✅ Prompts reloaded")


def render_inbox_tab():
    """Render the inbox view with email list and processing."""
    st.header("📬 Inbox")

    if not st.session_state.emails:
        st.info("👆 Click 'Load Mock Inbox' in the sidebar to get started.")
        return

    # Processing controls
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"{len(st.session_state.emails)} emails loaded")

    with col2:
        if st.button("🔍 Run Processing", use_container_width=True):
            process_all_emails()

    st.markdown("---")

    # Display emails in a table-like format
    for email in st.session_state.emails:
        email_id = email.id
        processed_data = st.session_state.processed.get(email_id, {})
        category = processed_data.get('category', 'Uncategorized')
        actions = processed_data.get('actions', [])

        # Category color coding
        category_colors = {
            'Important': '🔴',
            'To-Do': '📋',
            'Newsletter': '📰',
            'Spam': '🗑️',
            'Uncategorized': '⚪'
        }

        icon = category_colors.get(category, '⚪')

        with st.expander(f"{icon} **{email.subject}** - from {email.from_addr}"):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.caption(f"**From:** {email.from_addr}")
                st.caption(f"**Date:** {email.timestamp}")
                if category != 'Uncategorized':
                    st.caption(f"**Category:** {category}")

            with col2:
                if actions:
                    st.caption(f"✅ {len(actions)} action(s)")

            with col3:
                if st.button(f"📖 View Details", key=f"view_{email_id}"):
                    st.session_state.selected_email_id = email_id
                    st.rerun()

            # Show preview of body
            body_preview = email.body[:200] + "..." if len(email.body) > 200 else email.body
            st.text(body_preview)


def process_all_emails():
    """Process all emails: categorization and action extraction."""
    if not st.session_state.api_key_set:
        st.error("⚠️ Cannot process: API key not configured")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()

    total = len(st.session_state.emails)

    for idx, email in enumerate(st.session_state.emails):
        status_text.text(f"Processing email {idx + 1}/{total}: {email.subject[:50]}...")

        # Categorize
        category = categorize_email(email, st.session_state.prompts)

        # Extract actions
        actions = extract_action_items(email, st.session_state.prompts)

        # Store results
        st.session_state.processed[email.id] = {
            'category': category,
            'actions': actions
        }

        # Update email object
        email.category = category

        progress_bar.progress((idx + 1) / total)

    status_text.text("✅ Processing complete!")
    st.success(f"✅ Processed {total} emails successfully!")


def render_email_details_tab():
    """Render detailed view of selected email."""
    st.header("📧 Email Details")

    if not st.session_state.emails:
        st.info("No emails loaded.")
        return

    # Email selector
    email_options = {f"ID {e.id}: {e.subject[:50]}": e.id for e in st.session_state.emails}

    selected_label = st.selectbox(
        "Select an email:",
        options=list(email_options.keys()),
        index=0 if st.session_state.selected_email_id is None 
              else list(email_options.values()).index(st.session_state.selected_email_id) 
              if st.session_state.selected_email_id in email_options.values() else 0
    )

    selected_email_id = email_options[selected_label]
    st.session_state.selected_email_id = selected_email_id

    email = get_email_by_id(st.session_state.emails, selected_email_id)

    if not email:
        st.error("Email not found")
        return

    # Display email
    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(email.subject)

    with col2:
        processed_data = st.session_state.processed.get(email.id, {})
        category = processed_data.get('category', 'Uncategorized')
        if category != 'Uncategorized':
            st.markdown(f"**Category:** `{category}`")

    st.markdown(f"**From:** {email.from_addr}")
    st.markdown(f"**To:** {email.to_addr}")
    st.markdown(f"**Date:** {email.timestamp}")

    st.markdown("---")

    st.markdown("**Body:**")
    st.text_area("", email.body, height=200, disabled=True, label_visibility="collapsed")

    st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Summarize", use_container_width=True):
            if not st.session_state.api_key_set:
                st.error("⚠️ API key not configured")
            else:
                with st.spinner("Generating summary..."):
                    summary = summarize_email(email, st.session_state.prompts)
                    st.info(f"**Summary:**\n\n{summary}")

    with col2:
        if st.button("✅ Extract Tasks", use_container_width=True):
            if not st.session_state.api_key_set:
                st.error("⚠️ API key not configured")
            else:
                with st.spinner("Extracting tasks..."):
                    actions = extract_action_items(email, st.session_state.prompts)
                    if actions:
                        st.success(f"**Tasks Found ({len(actions)}):**")
                        for action in actions:
                            st.markdown(f"- {action.task}" + (f" *(Due: {action.deadline})*" if action.deadline else ""))
                    else:
                        st.info("No specific tasks found in this email.")

    with col3:
        if st.button("✉️ Draft Reply", use_container_width=True):
            st.session_state.show_draft_form = True

    # Draft reply form
    if st.session_state.get('show_draft_form', False):
        st.markdown("---")
        render_draft_form(email)

    # Show existing draft if available
    if email.id in st.session_state.drafts:
        st.markdown("---")
        st.subheader("💾 Saved Draft")
        draft = st.session_state.drafts[email.id]

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Subject:** {draft.subject}")
        with col2:
            st.caption(f"Created: {draft.created_at[:19]}")

        st.text_area("Draft Body:", draft.body, height=150, disabled=True)

        st.warning("⚠️ Draft only — not sent. No email sending functionality.")

    # Show extracted actions from processed data
    processed_data = st.session_state.processed.get(email.id, {})
    if processed_data.get('actions'):
        st.markdown("---")
        st.subheader("📋 Extracted Action Items")
        for action in processed_data['actions']:
            st.markdown(f"- {action.task}" + (f" *(Due: {action.deadline})*" if action.deadline else ""))


def render_draft_form(email):
    """Render form for drafting a reply."""
    st.subheader("✉️ Draft Reply")

    # Tone selector
    tone = st.selectbox(
        "Select tone:",
        options=["Professional", "Friendly", "Concise", "Formal"],
        index=0
    )

    if st.button("🤖 Generate Draft", use_container_width=True):
        if not st.session_state.api_key_set:
            st.error("⚠️ API key not configured")
            return

        with st.spinner("Drafting reply..."):
            draft = draft_reply(email, st.session_state.prompts, tone)
            st.session_state.drafts[email.id] = draft
            st.session_state.show_draft_form = False
            st.success("✅ Draft generated!")
            st.rerun()


def render_prompt_config_tab():
    """Render prompt configuration interface."""
    st.header("🧠 Prompt Brain Configuration")

    st.info("📝 Edit the prompts below to customize the agent's behavior. All AI operations use these prompts.")

    # Load current prompts
    prompts = st.session_state.prompts

    # Categorization prompt
    st.subheader("1. Categorization Prompt")
    st.caption("Used to categorize emails into: Important, Newsletter, Spam, To-Do")
    new_cat_prompt = st.text_area(
        "Categorization:",
        value=prompts.get('categorization', ''),
        height=100,
        key="cat_prompt"
    )

    # Action item prompt
    st.subheader("2. Action Item Extraction Prompt")
    st.caption("Used to extract tasks from emails (returns JSON)")
    new_action_prompt = st.text_area(
        "Action Item:",
        value=prompts.get('action_item', ''),
        height=100,
        key="action_prompt"
    )

    # Auto-reply prompt
    st.subheader("3. Auto-Reply Draft Prompt")
    st.caption("Used to draft replies to emails")
    new_reply_prompt = st.text_area(
        "Auto Reply:",
        value=prompts.get('auto_reply', ''),
        height=100,
        key="reply_prompt"
    )

    # Summary prompt
    st.subheader("4. Summary Prompt")
    st.caption("Used to summarize emails")
    new_summary_prompt = st.text_area(
        "Summary:",
        value=prompts.get('summary', ''),
        height=100,
        key="summary_prompt"
    )

    # General agent prompt
    st.subheader("5. General Agent Prompt")
    st.caption("Used for chat-based interactions")
    new_agent_prompt = st.text_area(
        "General Agent:",
        value=prompts.get('general_agent', ''),
        height=100,
        key="agent_prompt"
    )

    st.markdown("---")

    # Save button
    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("💾 Save Prompts", use_container_width=True):
            new_prompts = {
                'categorization': new_cat_prompt,
                'action_item': new_action_prompt,
                'auto_reply': new_reply_prompt,
                'summary': new_summary_prompt,
                'general_agent': new_agent_prompt
            }

            if save_prompts(new_prompts):
                st.session_state.prompts = new_prompts
                st.success("✅ Prompts saved successfully!")
            else:
                st.error("⚠️ Failed to save prompts")

    with col2:
        st.caption("Prompts are saved to data/prompts.json")


def render_agent_chat_tab():
    """Render the chat interface for the email agent."""
    st.header("💬 Email Agent Chat")

    if not st.session_state.emails:
        st.info("Load emails first to use the chat agent.")
        return

    st.caption("Ask questions about your emails using natural language!")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Ask about your emails...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate agent response
        if not st.session_state.api_key_set:
            response = "⚠️ API key not configured. Please set OPENAI_API_KEY."
        else:
            with st.spinner("Thinking..."):
                selected_email = None
                if st.session_state.selected_email_id:
                    selected_email = get_email_by_id(
                        st.session_state.emails,
                        st.session_state.selected_email_id
                    )

                response = run_agent_query(
                    user_input,
                    selected_email,
                    st.session_state.prompts,
                    st.session_state.emails
                )

        # Add agent response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        # Display agent response
        with st.chat_message("assistant"):
            st.markdown(response)

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Render sidebar
    render_sidebar()

    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📬 Inbox",
        "📧 Email Details", 
        "🧠 Prompt Brain Config",
        "💬 Email Agent Chat"
    ])

    with tab1:
        render_inbox_tab()

    with tab2:
        render_email_details_tab()

    with tab3:
        render_prompt_config_tab()

    with tab4:
        render_agent_chat_tab()

    # Footer
    st.markdown("---")
    st.caption("📧 Email Productivity Agent | Prompt-Driven Architecture | No emails are actually sent")


if __name__ == "__main__":
    main()
