"""
GPT Provider (OpenAI)

Writing and content generation capability.
"""

import os
from runtime.artifacts import Artifact

PROVIDER_NAME = "GPT-4o"
CAPABILITIES = ["writing"]


def execute(objective: str) -> Artifact:
    """
    Execute writing task using OpenAI GPT-4o.
    
    Requires OPENAI_API_KEY environment variable.
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("      GPT writing (mock - set OPENAI_API_KEY for real results)...")
        return _mock_write(objective)
    
    return _call_openai(objective, api_key)


def _call_openai(objective: str, api_key: str) -> Artifact:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are Precious, founder of CraftedWorkflows.
Write a personalized outreach message for this objective:

{objective}

Guidelines:
- Be respectful and concise
- Ask permission before pitching
- Mirror the prospect's language
- Diagnose before prescribing
- Keep it under 300 characters for DM

Return only the message text."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Precious, founder of CraftedWorkflows. Write concise, respectful outreach messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
    except Exception as e:
        content = f"GPT error: {e}"
    
    return Artifact(
        type="Draft",
        title="Outreach Message",
        content=content,
        created_by=PROVIDER_NAME
    )


def _mock_write(objective: str) -> Artifact:
    """Return mock draft for testing."""
    
    print("      GPT writing...")
    
    artifact = Artifact(
        type="Draft",
        title="Outreach Message",
        content=f"""Hey,

Quick question—has workload started growing faster than operational freedom recently?

—Precious""",
        created_by=PROVIDER_NAME
    )
    
    return artifact