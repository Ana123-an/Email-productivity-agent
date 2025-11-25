# 📧 Email Productivity Agent

A prompt-driven AI-powered email management system built with Streamlit and Python. Process emails, extract action items, draft replies, and interact with your inbox using natural language.
## ✨ Features

### 📥 Phase 1: Email Ingestion & Prompt Storage
- Load and process mock inbox with 15 diverse sample emails
- Edit and save AI prompt templates via intuitive UI
- Persistent configuration stored in JSON
- Never hard-codes prompts - all behavior driven by `prompts.json`

### 🤖 Phase 2: Email Processing Agent
- **Smart Categorization**: Automatically sorts emails (Important, Newsletter, Spam, To-Do)
- **Action Item Extraction**: Identifies tasks with deadlines
- **Email Summarization**: Generates 2-3 bullet point summaries
- **Natural Language Chat**: Query your inbox using conversational language

### ✉️ Phase 3: Draft Generation
- AI-powered reply drafting
- Customizable tone (Professional, Friendly, Formal, Concise)
- Draft storage and review (no actual sending for safety)
- Context-aware responses based on email thread

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or extract the project:**
unzip email-productivity-agent.zip
cd email-productivity-agent

2. **Install dependencies:**
pip install -r requirements.txt


3. **Set up your API key:**

**Option A: Environment Variable**
macOS/Linux
export OPENAI_API_KEY='your-api-key-here'

Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

**Option B: Create `.env` file**
cp .env.example .env

Edit .env and add your key:
OPENAI_API_KEY=your-api-key-here
MODEL_NAME=gpt-4o-mini

4. **Run the application:**
streamlit run app.py


5. **Open your browser:**
Navigate to `http://localhost:8501`

## 📖 Usage Guide

### Getting Started
1. Click **"🔄 Load Mock Inbox"** in the sidebar
2. Click **"🔍 Run Processing"** to categorize emails and extract actions
3. Explore the four main tabs

### Navigation

#### 📬 Inbox Tab
- View all emails with category tags
- See action item counts
- Quick access to email details
- Batch processing controls

#### 📧 Email Details Tab
Select and interact with individual emails:
- **Summarize**: Get a concise 2-3 bullet point summary
- **Extract Tasks**: Find action items with deadlines
- **Draft Reply**: Generate AI-powered responses with tone selection

#### 🧠 Prompt Brain Config Tab
Customize AI behavior:
- Edit all 5 prompt templates
- Control categorization logic
- Customize summarization style
- Modify reply drafting instructions
- Save changes to `prompts.json`

#### 💬 Email Agent Chat Tab
Natural language interaction:
"Summarize this email"
"What tasks do I need to do?"
"Show me all urgent emails"
"Draft a reply with friendly tone"


## 🏗️ Project Structure
email-productivity-agent/
├── app.py # Main Streamlit application
├── backend/ # Modular backend
│ ├── init.py
│ ├── models.py # Data models (Email, ActionItem, DraftEmail)
│ ├── inbox_loader.py # Email loading logic
│ ├── prompts_manager.py # Prompt CRUD operations
│ ├── processors.py # Email processing functions
│ ├── agent.py # Chat agent logic
│ └── llm_client.py # OpenAI API wrapper
├── data/
│ ├── mock_inbox.json # 15 sample emails
│ └── prompts.json # Editable prompt templates
├── requirements.txt # Python dependencies
└── .env.example # Environment variable template


## 🎯 Key Architecture Decisions

### Prompt-Driven Design
All AI behavior is controlled by user-editable prompts stored in `prompts.json`:
- **Categorization Prompt**: How emails are classified
- **Action Item Prompt**: Task extraction format (JSON)
- **Auto-Reply Prompt**: Reply drafting instructions
- **Summary Prompt**: Summarization style
- **General Agent Prompt**: Chat agent personality

### Modular Backend
Clear separation of concerns:
- `models.py`: Type-safe data structures
- `llm_client.py`: Centralized API calls with error handling
- `processors.py`: Email processing operations
- `agent.py`: Natural language query handling

### Safety First
- No actual email sending (drafts only)
- API keys via environment variables
- Comprehensive error handling
- JSON parsing with fallbacks

## 🌐 Deployment

### Streamlit Community Cloud (Recommended - FREE)

1. **Push to GitHub:**
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/email-agent.git
git push -u origin main


2. **Deploy:**
- Visit [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your repository
- Set main file: `app.py`
- Add secrets in "Advanced settings":

OPENAI_API_KEY = "your-api-key-here"
MODEL_NAME = "gpt-4o-mini"
- Click "Deploy"

3. **Done!** Your app will be live at `https://yourapp.streamlit.app`

### Docker Deployment
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


### Modifying Prompts
Use the **Prompt Brain Config** tab in the UI, or directly edit `data/prompts.json`

## 🐛 Troubleshooting

### "API Key not configured"
- Ensure `OPENAI_API_KEY` is set in environment or `.streamlit/secrets.toml`
- Restart the app after setting the key

### "Error loading inbox"
- Check that `data/mock_inbox.json` exists
- Validate JSON syntax

### "LLM Error: rate_limit"
- Wait a few seconds and try again
- Consider upgrading your OpenAI plan

### JSON Parsing Errors
- Review prompt templates in "Prompt Brain Config"
- Ensure `action_item` prompt requests valid JSON format

## 📊 Sample Data

The mock inbox includes 15 diverse emails:
- Meeting requests (for reply drafting)
- Newsletters (for categorization)
- Spam messages (for filtering)
- Task requests (for action extraction)
- Project updates (for summarization)
- HR notifications (with deadlines)
- Client inquiries (multi-question emails)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Connect to real email (Gmail API, IMAP)
- Calendar integration for meeting requests
- Email search and advanced filtering
- User authentication
- Multi-language support
- Export drafts to various formats

## 📄 License

This project is provided as-is for educational and productivity purposes.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web UI framework
- [OpenAI](https://openai.com/) - LLM API
- Python 3.10+

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review OpenAI API documentation
3. Verify all dependencies are installed correctly

## ⭐ Star this project!

If you find this helpful, please star the repository!

---

**Built with ❤️ using Streamlit, Python, and OpenAI**

*Last updated: November 25, 2025*


