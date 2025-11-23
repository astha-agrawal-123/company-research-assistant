from multi_source_retriever import MultiSourceRetriever
from account_plan_builder import AccountPlanBuilder
from agent import Agent
from company_classifier import CompanyClassifier


class ResearchManager:
    def __init__(self):
        self.retriever = MultiSourceRetriever()
        self.builder = AccountPlanBuilder()
        self.agent = Agent()
        self.classifier = CompanyClassifier()

    def start_research(self, company: str, session):
        session.append_log(f"Starting research: {company}")

        # ------------------ Fetch Wiki ------------------
        session.append_log("Fetching Wikipedia...")
        wiki = self.retriever.fetch_wikipedia(company)
        session.append_log(f"wiki: {wiki.get('title') or wiki.get('note') or wiki.get('error')}")

        # ------------------ Fetch Website ------------------
        session.append_log("Fetching website...")
        site = self.retriever.fetch_website_summary(company)
        session.append_log(f"site: {site.get('url') or site.get('note')}")

        # ------------------ Fetch News ------------------
        session.append_log("Fetching news...")
        news = self.retriever.fetch_news(company)
        if "articles" in news:
            session.append_log(f"news: {len(news['articles'])} articles")
        else:
            session.append_log(f"news: {news.get('note')}")

        raw = {"wiki": wiki, "site": site, "news": news}
        session.set("raw_research", raw)

        # ------------------ Classify Company ------------------
        session.append_log("Classifying entity (company/industry)...")
        profile = self.classifier.classify(company, raw)
        session.set("company_profile", profile)
        session.append_log(f"profile: {profile}")

        # ------------------ Summarize ------------------
        session.append_log("Summarizing with LLM...")
        synthesis = self.agent.summarize_research(raw)
        session.set("synthesis", synthesis)

        # ------------------ Build Plan ------------------
        session.append_log("Building account plan...")
        plan = self.builder.build_plan(company, synthesis, raw)
        plan["Company Profile"] = (
            f"Entity: {profile.get('entity_name')}\n"
            f"Is Company: {profile.get('is_company')}\n"
            f"Industry: {profile.get('industry')}\n"
            f"Confidence: {profile.get('confidence')}\n"
        )
        session.set("account_plan", plan)

        session.append_log("Research complete.")
        return plan

    # ------------------ Q/A ------------------
    def ask_question(self, question: str, session):
        raw = session.get("raw_research", {})
        plan = session.get("account_plan", {})
        profile = session.get("company_profile", {})

        context = {
            "raw_research": raw,
            "account_plan": plan,
            "company_profile": profile,
        }

        return self.agent.answer_question(question, context)

    def regenerate_section(self, section: str, session):
        synthesis = session.get("synthesis", "")
        return self.agent.regenerate_section(section, synthesis)

    def check_connection(self):
        return self.retriever.check_connectivity()
