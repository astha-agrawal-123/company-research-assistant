# Professional Company Research Assistant (Agentic Bot)

This project is an upgraded intermediate agentic research assistant that:
- Fetches data from Wikipedia, company websites, and news (with free scraping fallback)
- Synthesizes findings using a Groq LLM model
- Builds an editable account plan with sections: Overview, Key Executives, Products & Services, Financial Snapshot, SWOT, Recommended Strategy
- Provides the ability to regenerate specific sections using the LLM

## Quick start

1. Go to the path of the folder:
```bash
cd "Path-to-your-file"
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

## How to Generate a Groq API Key (Step-by-Step)
Follow these steps to create your Groq API key:

- Go to the official Groq Console: https://console.groq.com
- Sign in using your email or Google account.
- In the left sidebar, click on API Keys.
- Click the button “Create API Key”.
- Give your key a name (e.g., company-research-assistant).
- Click Generate.
- Copy the API key shown (it starts with gsk_...).
