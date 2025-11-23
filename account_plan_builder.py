import re

class AccountPlanBuilder:
    def build_plan(self, company, synthesis, raw):
        plan = {}

        # 1. Overview
        sources = []
        if raw.get("wiki", {}).get("summary"):
            sources.append("wiki")
        if raw.get("site", {}).get("url"):
            sources.append("site")
        if raw.get("news", {}).get("articles"):
            sources.append("news")

        plan["Company Overview"] = (
            synthesis + "\n\n(Sources used: " + ", ".join(sources) + ")"
        )

        # 2. Key executives
        plan["Key Executives"] = self._extract_execs(synthesis)

        # 3. Products & services
        plan["Products & Services"] = self._extract_products(synthesis)

        # 4. Financial Snapshot
        plan["Financial Snapshot"] = (
            "No financial data was found. Use Yahoo Finance or MarketStack API for revenue/profit."
        )

        # 5. SWOT
        plan["SWOT Analysis"] = self._swot(synthesis)

        # 6. Recommendations
        plan["Recommended Strategy"] = self._recommend()

        return plan

    def _extract_execs(self, text):
        titles = ["CEO", "Founder", "CFO", "CTO", "COO", "Chairman"]
        lines = text.splitlines()
        found = [l.strip() for l in lines if any(t in l for t in titles)]
        return "\n".join(found) if found else "Executives not detected."

    def _extract_products(self, text):
        words = ["product", "service", "platform", "technology", "device", "solution"]
        lines = text.splitlines()
        found = [l.strip() for l in lines if any(w in l.lower() for w in words)]
        return "\n".join(found[:6]) if found else "Products/services not detected."

    def _swot(self, text):
        S = ["Strong market presence"]
        W = ["Gaps in public financial data"]
        O = ["Growth opportunities in core products"]
        T = ["Competitive threats in industry"]

        return (
            "Strengths:\n- " + "; ".join(S) +
            "\nWeaknesses:\n- " + "; ".join(W) +
            "\nOpportunities:\n- " + "; ".join(O) +
            "\nThreats:\n- " + "; ".join(T)
        )

    def _recommend(self):
        return (
            "1) Validate all strategic claims via financial APIs.\n"
            "2) Identify decision-makers using executive detection.\n"
            "3) Focus outreach on high-value product segments.\n"
            "4) Monitor competitor movements.\n"
        )
