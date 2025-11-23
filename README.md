# Professional Company Research Assistant (Agentic Bot)

This project is an upgraded intermediate agentic research assistant that:
- Fetches data from Wikipedia, company websites, and news (with free scraping fallback)
- Synthesizes findings using a Groq LLM model
- Builds an editable account plan with sections: Overview, Key Executives, Products & Services, Financial Snapshot, SWOT, Recommended Strategy
- Provides the ability to regenerate specific sections using the LLM

## Quick start

1. Create a python virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows (cmd)
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set environment variables (or create a `.env` file):
```bash
export GROQ_API_KEY="your_groq_api_key"
export GROQ_MODEL="llama-3.3-70b-versatile"  # or a model listed by your account
```

4. Run the app:
```bash
streamlit run app.py
```

## Notes
- If your Groq key lacks access to a model, run `list_models.py` to see available models.
- The news scraping fallback is lightweight (HTML scraping) and may miss JavaScript-heavy sites.
- For production use, add caching, rate-limiting, and secure storage of API keys.
