# Company Research Assistant — Account Plan Generator

## Overview
This is a simple Company Research Assistant that synthesizes data into an account plan.
It is a demo project for the Eightfold.ai Agentic AI assignment.

### Features
- Retrieves company intro from Wikipedia
- Synthesizes a structured account plan using OpenAI LLM
- Suggests follow-up questions
- Allows inline edits and plan export (JSON)

## Requirements
- Python 3.9+
- pip install -r requirements.txt
- Set your OpenAI key: `export OPENAI_API_KEY="sk-..."` (or use .env)

## How to run
1. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
Set API key:

export OPENAI_API_KEY="YOUR_KEY"


Start the app:

streamlit run app.py

Files

app.py — Streamlit UI

agent.py — orchestration and LLM calls

retriever.py — Wikipedia retrieval

prompts.py — prompt templates

demo_script.md — instructions for recording your demo

Notes & limitations

Wikipedia is used for retrieval; integrate a News/SERP API for production.

The app demonstrates agentic behaviour via follow-ups and user edits.

The uploaded assignment screenshot used in the UI:
/mnt/data/B77BC0A1-9F46-4749-9235-2DED012A3769.jpeg

How this meets evaluation criteria

Conversational quality: follow-up prompts + editable plan

Agentic behaviour: asks clarifying questions and updates plan

Technical implementation: LLM + retrieval pipeline

Intelligence & adaptability: heuristics + LLM-based plan update


---

# 6) Demo script — what to record (`demo_script.md`)
```markdown
Demo sequence (max 10 minutes):

1. Intro (10s)
   - "Hi — this demo shows the Company Research Assistant building an account plan for a company."

2. Show inputs (15s)
   - Type "Zoom Video Communications" (or choose any company).
   - Add context: "Prepare an account plan to approach their sales team."

3. Generate plan (1:30)
   - Click "Generate Plan"
   - Show spinner, then the generated plan in UI.

4. Highlight sections (1:00)
   - Point out Overview, Market Position, Key Products, Recent News, Financial Snapshot, Risks, Recommended Next Steps.

5. Show follow-ups (1:00)
   - Show suggested follow-up question(s) like "Do you want me to search for financials?"
   - Answer the follow-up (type a reply) and click "Ask follow-ups & update plan".

6. Edit plan (1:00)
   - Edit Key Products inline (simulate user corrections).
   - Export as JSON -> show file saved.

7. Edge-case test (1:30)
   - Enter a small startup name that might not have a Wikipedia page.
   - Show how the agent asks clarifying questions or says "Not found".

8. Conclude (10s)
   - "This demonstrates natural interaction, follow-up capability, and editable plan export."

Tips:
- Keep voiceover concise; narrate steps as they happen.
- Show multiple personas quickly (e.g., "Confused user" ask: 'What does this company do?'; "Efficient user" ask: 'Give me 3 bullets for outreach').
