"""
Browser Provider

Web search and scraping capability.
"""

import os
import requests
from runtime.artifacts import Artifact

PROVIDER_NAME = "Browser"
CAPABILITIES = ["research"]


def execute(objective: str) -> Artifact:
    """
    Execute web search for the given objective.
    
    Uses SerpAPI if available, otherwise returns mock data.
    """
    
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    if serpapi_key:
        return _search_serpapi(objective, serpapi_key)
    else:
        print("      Browser searching (mock - set SERPAPI_KEY for real results)...")
        return _mock_search(objective)


def _search_serpapi(query: str, api_key: str) -> Artifact:
    """Search using SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for result in data.get("organic_results", [])[:10]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            link = result.get("link", "")
            results.append(f"{title}\n{snippet}\n{link}")
        
        content = "\n\n".join(results) if results else "No results found."
        
    except Exception as e:
        content = f"Search error: {e}"
    
    return Artifact(
        type="Research",
        title=f"Browser Search: {query[:50]}",
        content=content,
        created_by=PROVIDER_NAME
    )


def _mock_search(objective: str) -> Artifact:
    """Return mock lead data for testing."""
    
    print("      Browser searching...")
    
    artifact = Artifact(
        type="LeadList",
        title="Potential Leads",
        content="""Agency Alpha|Marketing Agency|London|12 Employees
Agency Bravo|Creative Agency|Manchester|7 Employees
Agency Charlie|Automation Agency|Birmingham|4 Employees
Agency Delta|Web Design Agency|London|22 Employees
Agency Echo|SEO Agency|Leeds|9 Employees""",
        created_by=PROVIDER_NAME
    )
    
    return artifact