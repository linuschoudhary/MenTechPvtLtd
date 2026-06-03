from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

MAX_RESULTS = 5


BLOCKED_DOMAINS = [
    "facebook.com", "twitter.com", "x.com",
    "instagram.com", "pinterest.com",
    "youtube.com", "reddit.com",
    "linkedin.com", "quora.com"
]




def search_internet_using_ddgs(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=MAX_RESULTS))

    except Exception as e:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=MAX_RESULTS))
        except:
            results = ""

    final_results =  [
        {
            "url": result.get("href") or result.get("url") or "",
        }
        for result in results
    ]
    return final_results


def is_valid(url):
    return not any(b in url for b in BLOCKED_DOMAINS)


def get_page_text(url):
    valid_url = is_valid(url)
    try:
        if valid_url:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove scripts/styles
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            paragraphs = soup.find_all("p")
            text = "\n".join(p.get_text() for p in paragraphs)
            return text

    except requests.RequestException as e:
        return ""
    

def search_internet(**query: str) -> dict:
    query = query["query"]
    results = search_internet_using_ddgs(query=query)

    news_dict = {}
    print("got some sites to search on...")
    for r in results:
        print(f"URL: {r['url']}")

        text = get_page_text(
            r['url']
        )
        news_dict[r["url"]] = text

    result = ""
    for value in news_dict.values():
        try:
            result += value
        except Exception as e:
            result += "" 

    return result

# search_internet(query="what is the current situation of us-iran war?")