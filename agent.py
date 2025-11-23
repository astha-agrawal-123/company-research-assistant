# agent.py
import os
import openai
import json
from retriever import fetch_wikipedia, fetch_news_headlines
from prompts import SYNTHESIS_PROMPT

openai.api_key = os.getenv("OPENAI_API_KEY")  # put your key in env

class CompanyAgent:
    def __init__(self, model="gpt-4o-mini" ):
        # You can change model to text-davinci-003 or gpt-4o depending on access.
        self.model = model

    def _call_llm(self, prompt, temperature=0.0, max_tokens=800):
        # Basic wrapper
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"system", "content":"You are a helpful assistant."},
                      {"role":"user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return resp['choices'][0]['message']['content']

    def generate_account_plan(self, company_name, context=""):
        # 1) Retrieve
        wiki = fetch_wikipedia(company_name)
        news = fetch_news_headlines(company_name)
        sources = []
        if wiki:
            sources.append(f"Wikipedia ({wiki['url']}):\n{wiki['intro'][:2000]}")
        else:
            sources.append("No Wikipedia page found.")
        if news:
            sources.append("News Headline Summaries:\n" + "\n".join(news))
        sources_text = "\n\n".join(sources) + "\n\nContext: " + context

        # 2) Create prompt and call LLM
        prompt = SYNTHESIS_PROMPT.format(sources_text=sources_text)
        out = self._call_llm(prompt)
        # LLM returns JSON — try to parse
        try:
            parsed = json.loads(out)
        except Exception:
            # if parsing fails, attempt to extract json substring
            import re
            m = re.search(r"\{.*\}", out, re.S)
            if m:
                parsed = json.loads(m.group(0))
            else:
                parsed = {"company": company_name, "Overview": out, "Market_Position": "Not found",
                          "Key_Products":"Not found","Recent_News":"Not found","Financial_Snapshot":"Not found",
                          "Risks":"Not found","Recommended_Next_Steps":"Not found"}
        # 3) Ask LLM for follow-ups if missing or conflicting
        followups = self._generate_followups(parsed)
        return parsed, followups

    def _generate_followups(self, parsed_plan):
        # Simple heuristics: if core sections are "Not found" -> followups
        followups = []
        if parsed_plan.get("Financial_Snapshot", "") in [None, "", "Not found"]:
            followups.append("Do you want me to search for financial reports or approximate revenue figures?")
        if parsed_plan.get("Key_Products", "") in [None, "", "Not found"]:
            followups.append("Which product lines are you most interested in (platform, services, hardware)?")
        # also if overview is short:
        if len(parsed_plan.get("Overview","")) < 80:
            followups.append("Would you like a longer company overview including its history and founding details?")
        return followups

    def update_plan_with_followups(self, plan, answers):
        # incorporate answers by asking LLM to update plan with the new info
        augment_text = "User answers to follow-up questions:\n" + "\n".join(answers) + "\n\nCurrent plan:\n" + json.dumps(plan)
        prompt = "Update the existing JSON account plan with the user's answers. If new info resolves missing sections, fill them. Return only updated JSON.\n\n" + augment_text
        out = self._call_llm(prompt)
        try:
            new_plan = json.loads(out)
        except Exception:
            import re
            m = re.search(r"\{.*\}", out, re.S)
            if m:
                new_plan = json.loads(m.group(0))
            else:
                new_plan = plan
        return new_plan

    def plan_to_markdown(self, plan):
        md = f"## {plan.get('company','')}\n\n"
        for k in ["Overview","Market_Position","Key_Products","Recent_News","Financial_Snapshot","Risks","Recommended_Next_Steps"]:
            v = plan.get(k, "")
            md += f"### {k.replace('_',' ')}\n{v}\n\n"
        return md
