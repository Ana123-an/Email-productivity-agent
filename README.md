📧 Prompt-Driven Email Productivity Agent

An intelligent LLM-powered Email Productivity Agent that automates inbox management.
The system uses user-defined prompts (“Prompt Brain”) to categorize emails, extract action items, summarize content, and auto-draft replies — all through a clean Streamlit interface.

🚀 Features
Capability	Description
Email Categorization	Classifies emails into Important / To-Do / Newsletter / Spam
Action-Item Extraction	Identifies tasks + deadlines and stores them in structured format
Auto-Draft Replies	Generates editable draft responses (never sends emails)
Chat-Based Interaction	Ask: “Summarize this email”, “What tasks do I have?” etc.
Prompt-Driven System	User-editable configuration that shapes agent behavior
Error Safe	Fallback responses if LLM/API issues occur

All results are stored safely in session state — no email is sent automatically.

🏗️ System Architecture
Streamlit Frontend
   │
   ├── Inbox Viewer
   ├── Email Details
   ├── Prompt Manager
   └── Email Agent Chat
   │
Python Backend
   ├── LLM Client (OpenAI/Compatible)
   ├── Inbox Loader
   ├── Prompt Storage Layer
   ├── Processing Agent
   └── Draft Manager


Prompts drive ALL LLM behavior and are stored in a JSON file that the user can edit anytime.

📂 Project Structure
email-productivity-agent/
│
├── app.py                        # Streamlit UI
├── backend/
│   ├── models.py
│   ├── inbox_loader.py
│   ├── processors.py
│   ├── prompts_manager.py
│   ├── llm_client.py
│   └── agent.py
├── data/
│   ├── mock_inbox.json           # 10–20 sample emails
│   └── prompts.json              # Editable prompts ("Prompt Brain")
├── requirements.txt
└── .env.example (optional)

🛠️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/<your-user>/email-productivity-agent.git
cd email-productivity-agent

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure LLM API Key

Create a .env file / Streamlit Secrets:

OPENAI_API_KEY="your-key-here"

4️⃣ Run the Application
streamlit run app.py

📥 Loading the Mock Inbox

The app includes a mock inbox stored at:

data/mock_inbox.json


To load it:

Launch the app

Click “Load Mock Inbox”

The Inbox tab will show all sample emails

🎛️ Prompt Configuration (Prompt Brain)

To customize how the AI behaves:

Open the Prompt Manager tab (or sidebar)

Edit prompts such as:

Categorization Prompt

Action-Item Extraction Prompt

Auto-Reply Draft Prompt

Summary Prompt

Click “Save Prompts” to update the system instantly

This enables dynamic behavior change without editing code.

💡 Usage Guide
📨 Inbox Tab

Load mock inbox

View sender, subject, timestamp

Run full processing (categorization + action extraction)

🔍 Email Details Tab

Select an email to view full content

Buttons available:

Summarize Email

Show Action Items

Draft Reply → Editable + Save as draft

🤖 Email Agent Chat Tab

Ask conversational questions like:

Query Type	Example
Summarization	“Summarize this email”
Task Recall	“What tasks do I need to do today?”
Priority Help	“Show all Important emails”
Draft Writing	“Reply in a more formal tone”

The agent uses:

User-defined prompts

Inbox context

Email thread content

🔐 Safety & Robustness

✔ No emails are sent — only drafts saved
✔ LLM errors are caught and shown gracefully
✔ JSON parsing fallback for invalid model outputs
✔ User stays in control of final email content

📹 Demo Video Requirements (for submission)

Record a 5–10 minute walkthrough showing:

Requirement	Demonstrate
Loading Inbox	Show mock inbox loading UI
Editing Prompts	Modify prompt and reprocess
Categorization + Action Extraction	Run processing, show tags and tasks
Chat-Based Actions	Summarize, reply, suggest actions

Optional: Highlight draft storage + safety features

📌 Evaluation Criteria Checklist (✔ Completed)
Requirement	Status
Inbox ingestion	✔
Prompt-driven behavior	✔
Summaries, replies, actions	✔
Drafts only	✔
UI clarity + good UX	✔
Error handling	✔
Modular architecture	✔
👤 Author

Ananya Mishra
Email: mishra77ananya@gmail.com
