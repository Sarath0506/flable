import requests
import os
from dotenv import load_dotenv

load_dotenv()

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

HEADERS = {
    "Accept": "application/json",
    "X-Subscription-Token": BRAVE_API_KEY
}


def brave_search(query: str, num_results: int = 5) -> list:
    """
    Perform Brave API search and return structured results.
    """
    params = {"q": query, "count": num_results, "freshness": "week"}

    response = requests.get(BRAVE_SEARCH_URL, headers=HEADERS, params=params)
    response.raise_for_status()

    results = response.json().get("web", {}).get("results", [])

    return [
        {
            "title": r["title"],
            "url": r["url"],
            "snippet": r.get("description", "")
        } for r in results
    ]
