# retriever.py
import requests
from bs4 import BeautifulSoup
import re

def fetch_wikipedia(company_name):
    """
    Fetch the intro and infobox-like data from Wikipedia page if available.
    Returns a dict {'title':..., 'intro':..., 'raw_html':...}
    """
    # simple wiki search via opensearch
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'opensearch',
        'search': company_name,
        'limit': 1,
        'namespace': 0,
        'format': 'json'
    }
    r = requests.get(search_url, params=params, timeout=10)
    data = r.json()
    if len(data) >= 2 and data[1]:
        page_title = data[1][0]
    else:
        return None
    # fetch page content
    page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
    r2 = requests.get(page_url, timeout=10)
    soup = BeautifulSoup(r2.text, 'html.parser')
    # intro paragraphs
    paras = soup.select("div.mw-parser-output > p")
    intro = ""
    for p in paras:
        text = p.get_text().strip()
        if text:
            intro += text + "\n\n"
        # break after a couple paras to avoid huge intro
        if len(intro) > 1000:
            break
    return {
        'title': page_title,
        'url': page_url,
        'intro': intro,
        'raw_html': r2.text
    }

# placeholder for news/serp retrieval — for the assignment you can leave this optional
def fetch_news_headlines(company_name, max_articles=5):
    """
    Placeholder: For production, plug a News API or SERP API.
    Currently returns an empty list. Example: integrate SerpAPI or Google News API.
    """
    return []
