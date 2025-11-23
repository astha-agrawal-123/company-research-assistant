import json
import re
from agent import Agent


class CompanyClassifier:
    def __init__(self):
        self.agent = Agent()

    def classify(self, name, raw):
        profile = {
            "entity_name": name,
            "is_company": False,
            "industry": "unknown",
            "confidence": 0.0,
            "notes": "",
        }

        wiki = raw.get("wiki", {})
        site = raw.get("site", {})
        news = raw.get("news", {})

        def score(text, words):
            if not text:
                return 0
            text = text.lower()
            return sum(1 for w in words if w in text)

        business_words = [
            "company", "inc", "corporation", "limited", "llc", "group", "industry",
            "technology", "bank", "finance", "software", "platform", "services"
        ]

        s = 0
        s += score(wiki.get("summary", ""), business_words) * 2
        s += score(site.get("snippet", ""), business_words)
        if news.get("articles"):
            headlines = " ".join(a["title"] for a in news["articles"])
            s += score(headlines, business_words)

        if s >= 2:
            profile["is_company"] = True
            profile["confidence"] = min(0.9, 0.3 + s * 0.15)

        # Industry detection
        industries = {
            "technology": ["tech", "software", "cloud", "ai", "device", "chip"],
            "finance": ["bank", "loan", "insurance"],
            "retail": ["store", "retail", "ecommerce"],
            "energy": ["oil", "gas", "refinery", "energy"],
            "healthcare": ["health", "medical", "pharma", "drug"],
        }

        for ind, keywords in industries.items():
            if score(wiki.get("summary", ""), keywords) > 0 or score(site.get("snippet", ""), keywords) > 0:
                profile["industry"] = ind
                break

        # If low confidence → use LLM
        if profile["confidence"] < 0.5:
            llm_result = self.agent.classify_company_with_llm(raw, name)
            try:
                parsed = json.loads(llm_result)
                profile.update(parsed)
            except:
                if "company" in llm_result.lower():
                    profile["is_company"] = True
                profile["notes"] = llm_result[:500]

        return profile
