# Company Research Assistant — Account Plan Generator

## Overview
This is a simple Company Research Assistant that synthesizes data into an account plan.
It is a demo project for the Eightfold.ai Agentic AI assignment.

### Features
- Retrieves company intro from Wikipedia
- Synthesizes a structured account plan using OpenAI LLM
- Suggests follow-up questions
- Allows inline edits and plan export (JSON)

## 📂 Project Structure

* `app.py` — Main Streamlit User Interface.
* `agent.py` — Logic for orchestration and LLM API calls.
* `retriever.py` — Wikipedia retrieval logic.
* `prompts.py` — System prompts and template management.
* `demo_script.md` — Instructions/Sequence for recording the project demo.

## 🛠️ Installation & Setup

**1. Clone the repository and set up the environment:**

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

**2. Configure your API Key:
