import os
import json
from groq import Groq
from prompts import (
    SYSTEM_RESEARCH_PROMPT,
    USER_SYNTHESIS_PROMPT,
    QA_PROMPT_TEMPLATE,
    REGENERATE_SECTION_PROMPT,
    CLASSIFY_PROMPT,
)

# Initialize Groq client
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

# Default model — override via env GROQ_MODEL
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class Agent:
    def __init__(self):
        self.client = client
        self.model = MODEL

    def _chat(self, messages, temperature=0.2, max_tokens=800):
        if self.client is None:
            return "⚠️ Groq key not set. Set GROQ_API_KEY."

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()

        except Exception as e:
            err = str(e)

            # Suggest available models
            if "model_not_found" in err:
                try:
                    models = self.client.models.list()
                    ids = [m.id for m in models.data]
                    return (
                        f"⚠️ Invalid model.\nError: {err}\n"
                        f"Available models: {ids[:5]}"
                    )
                except Exception:
                    return f"⚠️ Groq error: {err}"

            return f"⚠️ Groq API Error: {err}"

    # --------------------------------------------------------
    # Summaries
    # --------------------------------------------------------
    def summarize_research(self, raw_research):
        raw_json = json.dumps(raw_research, indent=2, ensure_ascii=False)
        messages = [
            {"role": "system", "content": SYSTEM_RESEARCH_PROMPT},
            {"role": "user", "content": USER_SYNTHESIS_PROMPT.format(raw=raw_json)},
        ]
        return self._chat(messages, temperature=0.1, max_tokens=1500)

    # --------------------------------------------------------
    # Q & A
    # --------------------------------------------------------
    def answer_question(self, question, context):
        ctx = json.dumps(context, indent=2, ensure_ascii=False)
        messages = [
            {"role": "system", "content": SYSTEM_RESEARCH_PROMPT},
            {"role": "user", "content": QA_PROMPT_TEMPLATE.format(question=question, context=ctx)},
        ]
        return self._chat(messages, temperature=0.2, max_tokens=600)

    # --------------------------------------------------------
    # Regenerate Section
    # --------------------------------------------------------
    def regenerate_section(self, section, synthesis):
        messages = [
            {"role": "system", "content": SYSTEM_RESEARCH_PROMPT},
            {"role": "user", "content": REGENERATE_SECTION_PROMPT.format(section=section, synthesis=synthesis)},
        ]
        return self._chat(messages, temperature=0.2, max_tokens=600)

    # --------------------------------------------------------
    # Company Classification
    # --------------------------------------------------------
    def classify_company_with_llm(self, raw_research, company_name):
        raw_json = json.dumps(raw_research, indent=2, ensure_ascii=False)
        messages = [
            {"role": "system", "content": "You classify entities as companies and detect industry."},
            {"role": "user", "content": CLASSIFY_PROMPT.format(company=company_name, raw=raw_json)},
        ]
        return self._chat(messages, temperature=0.0, max_tokens=350)
