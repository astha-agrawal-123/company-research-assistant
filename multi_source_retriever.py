import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import os

# Global headers for all requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0 Safari/537.36 ResearchBot/1.0"
    )
}

class MultiSourceRetriever:

    def __init__(self):
        # Two fallback sources (Google News + DuckDuckGo)
        self.news_sources = [
            "https://www.google.com/search?tbm=nws&q={query}",
            "https://duckduckgo.com/html/?q={query}"
        ]

    # -------------------------------------------------------------------------
    # 1) Wikipedia Fetch — Safe, Entity-resolved (Apple → Apple Inc.)
    # -------------------------------------------------------------------------
    def fetch_wikipedia(self, company: str):
        """
        Fetch only COMPANY-related Wikipedia pages.
        Forces '(company)' suffix for accurate corporate results.
        """
        try:
            safe_title = f"{company} (company)"
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(safe_title)}"

            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                data = r.json()

                # Validate that page is actually about a company
                extract = data.get("extract", "").lower()
                if any(keyword in extract for keyword in ["company", "corporation", "inc", "limited", "technology", "software"]):
                    return {
                        "title": data.get("title"),
                        "summary": data.get("extract"),
                        "url": data.get("content_urls", {}).get("desktop", {}).get("page")
                    }

            # Fallback: generic title
            fallback_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(company)}"
            r2 = requests.get(fallback_url, headers=HEADERS, timeout=10)

            if r2.status_code == 200:
                data = r2.json()
                return {
                    "title": data.get("title"),
                    "summary": data.get("extract"),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page")
                }

            return {"error": f"wiki {r.status_code}", "note": "No valid company wiki page found."}

        except Exception as e:
            return {"error": str(e)}

    # -------------------------------------------------------------------------
    # 2) Website Fetch — Smart domain guessing + de-promo cleaning
    # -------------------------------------------------------------------------
    def fetch_website_summary(self, company: str):
        # Trial domains
        candidates = [
            f"https://{company.lower()}.com",
            f"https://www.{company.lower()}.com",
            f"https://{company.lower()}.co",
            f"https://{company.lower()}.co.in",
        ]

        for url in candidates:
            try:
                r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)

                if r.status_code == 200 and len(r.text) > 300:
                    soup = BeautifulSoup(r.text, "html.parser")

                    title = soup.title.string.strip() if soup.title else url

                    # Meta description extract
                    meta_tag = (
                        soup.find("meta", attrs={"name": "description"}) or
                        soup.find("meta", attrs={"property": "og:description"}) or
                        soup.find("meta", attrs={"name": "og:description"})
                    )
                    meta_desc = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else ""

                    # Extract visible text
                    visible_text = " ".join(soup.get_text(separator=" ").split())
                    visible_text = visible_text[:3000]  # Limit

                    # Remove promotions / gift card offers
                    blacklist = ["sale", "discount", "gift card", "shopping event", "promo", "offer", "deal"]
                    if any(b in visible_text.lower() for b in blacklist):
                        # Filter promotional lines
                        cleaned = "\n".join(
                            line for line in visible_text.split(".")
                            if not any(b in line.lower() for b in blacklist)
                        )
                        visible_text = cleaned

                    return {
                        "url": url,
                        "title": title,
                        "description": meta_desc,
                        "snippet": visible_text
                    }

            except Exception:
                continue

        return {"note": "No company website found with heuristics."}

    # -------------------------------------------------------------------------
    # 3) News Fetch — Google News + DuckDuckGo (FREE)
    # -------------------------------------------------------------------------
    def fetch_news(self, company: str):
        articles = []

        for src in self.news_sources:
            try:
                url = src.format(query=quote(company + " company"))
                r = requests.get(url, headers=HEADERS, timeout=10)

                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, "html.parser")

                # Extract article-like links
                for a in soup.find_all("a", href=True):
                    text = a.get_text(strip=True)
                    href = a["href"]

                    if len(text) < 25:
                        continue  # skip junk links

                    # Fix partial Google links
                    if href.startswith("/"):
                        href = "https://www.google.com" + href

                    # Clean out irrelevant domains
                    if "google" in href and "news" not in href:
                        continue

                    articles.append({"title": text, "url": href})

                if articles:
                    break  # stop after first good source

            except Exception:
                continue

        if not articles:
            return {"note": "No news articles found (fallback scrape)."}

        return {"articles": articles[:8]}  # top 8

    # -------------------------------------------------------------------------
    # 4) Connectivity Check
    # -------------------------------------------------------------------------
    def check_connectivity(self):
        try:
            r = requests.get("https://api.groq.com", timeout=5)
            return {"groq_api": r.status_code}
        except Exception as e:
            return {"groq_api_error": str(e)}
