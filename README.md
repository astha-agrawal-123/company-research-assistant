# Company Research Assistant — Account Plan Generator

## Overview
This is a simple Company Research Assistant that synthesizes data into an account plan. It is a demo project for the **Eightfold.ai Agentic AI assignment**.

## Features
- Retrieves company intro from Wikipedia
- Synthesizes a structured account plan using OpenAI LLM
- Suggests follow-up questions
- Allows inline edits and plan export (JSON)

## Requirements
- Python 3.9+
- `pip install -r requirements.txt`
- Set your OpenAI key: `export OPENAI_API_KEY="sk-..."` (or use .env)

## How to run

**1. Install dependencies:**

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**2. Set API key:**

```bash
export OPENAI_API_KEY="YOUR_KEY"
```

**2. Start the app:**

```bash
streamlit run app.py
```

## Files

- app.py — Streamlit UI
- agent.py — orchestration and LLM calls
- retriever.py — Wikipedia retrieval
- prompts.py — prompt templates
- demo_script.md — instructions for recording your demo
