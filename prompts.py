SYSTEM_RESEARCH_PROMPT = """
You are a professional B2B research assistant.
Your job:
- Identify the correct company (ignore irrelevant meanings like fruits, places, etc.)
- Produce clear, business-focused summaries
- Avoid promotional garbage scraped from websites
"""

USER_SYNTHESIS_PROMPT = """
Raw scraped data:
{raw}

Your job:
1. Identify the *correct* company entity.
2. Ignore irrelevant text (fruit definitions, ads, promotions, gift cards).
3. Produce a 3–6 paragraph high-quality company summary.
4. Then produce:
   - Key Facts
   - Unknowns to Verify
   - Top 5 Actionable Insights
"""

QA_PROMPT_TEMPLATE = """
Context:
{context}

Question:
{question}

Instructions:
- Answer ONLY using relevant company/business context.
- Ignore products, promotions, fruit definitions, unrelated text.
- If something is missing, state what additional info would be needed.
"""

REGENERATE_SECTION_PROMPT = """
Synthesis:
{synthesis}

Regenerate section:
{section}

Rules:
- Keep it business-focused.
- Provide 2–4 sentences + bullet points.
"""

CLASSIFY_PROMPT = """
Determine if the following is a company. Output JSON.

Company name: {company}
Raw data: {raw}

Return JSON:
{
  "entity_name": "...",
  "is_company": true/false,
  "industry": "<one word>",
  "confidence": <0 to 1>,
  "notes": "..."
}
"""
