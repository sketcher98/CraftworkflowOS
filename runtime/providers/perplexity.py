"""
Perplexity Provider

Deep research and ICP matching capability.
"""

import os
from runtime.artifacts import Artifact

PROVIDER_NAME = "Perplexity"
CAPABILITIES = ["research"]


def execute(objective: str) -> Artifact:
    """
    Execute research using Perplexity API.
    
    Requires PERPLEXITY_API_KEY environment variable.
    """
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        print("      Perplexity researching (mock - set PERPLEXITY_API_KEY for real results)...")
        return _mock_research(objective)
    
    return _call_perplexity(objective, api_key)


def _call_perplexity(objective: str, api_key: str) -> Artifact:
    """Call Perplexity API for deep research."""
    try:
        import requests
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Research this objective for CraftedWorkflows (AI systems for service businesses):

{objective}

Find:
1. Companies matching our ICP (agencies, consultancies, creative studios, 2-15 employees, UK-based)
2. Specific buying signals (hiring, scaling, operational pain, delivery bottlenecks)
3. Founder/decision maker names and LinkedIn profiles
4. Recent company news/posts indicating growth pain

Return structured data with company, industry, location, size, buying signals, and LinkedIn URLs."""
        
        payload = {
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "You are a lead intelligence specialist for CraftedWorkflows. Find high-quality agency founders with operational scaling pain."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.2
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        
    except Exception as e:
        content = f"Perplexity error: {e}"
    
    return Artifact(
        type="Research",
        title="ICP Research",
        content=content,
        created_by=PROVIDER_NAME
    )


def _mock_research(objective: str) -> Artifact:
    """Return mock research for testing."""
    
    print("      Perplexity researching...")
    
    artifact = Artifact(
        type="Research",
        title="ICP Research",
        content=f"""Research summary for:

{objective}

Recommended targets:

• Creative agencies
• Marketing agencies
• Automation consultancies
• Brand studios
• Web development shops

Buying signals to watch:
- Hiring announcements
- "Booked out" posts
- Operational scaling complaints
- Delivery bottleneck mentions""",
        created_by=PROVIDER_NAME
    )
    
    return artifact