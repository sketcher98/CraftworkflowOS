#!/usr/bin/env python3
"""
Daily Commercial Briefing

Runs the complete commercial pipeline and outputs actionable outreach messages.
This is the primary revenue-generating workflow for Hermes COO.
"""

from runtime.context import OperatingContext
from runtime.loader import load_company, refresh_runtime
from runtime.commercial import discovery, lead_intelligence
from runtime.outreach import create_messages
from runtime.task import Task


def run_commercial_briefing(runtime=None):
    """
    Execute the full commercial pipeline and return formatted briefing.
    """
    if runtime is None:
        runtime = OperatingContext()
    
    # Load company knowledge
    runtime = load_company(runtime)
    
    # Refresh dynamic context (inbox, projects, clients)
    runtime = refresh_runtime(runtime, tier="warm")
    
    # Create discovery task
    task = Task(
        objective="Find high-quality agency founders matching ICP for outreach today",
        department="Commercial"
    )
    
    # Run discovery (research + writing capabilities)
    print("🔍 Running Discovery...")
    result = discovery(task)
    
    # Collect artifacts from all providers
    artifacts = []
    for step in result["steps"]:
        artifacts.extend(step["providers"])
    
    # Run lead intelligence (scoring against ICP)
    print("🧠 Running Lead Intelligence...")
    qualified = lead_intelligence(artifacts)
    
    # Generate outreach messages via Commercial Brain
    print("✍️  Generating Outreach Messages...")
    messages = create_messages(qualified)
    
    # Format briefing
    briefing = format_briefing(qualified, messages)
    
    return briefing, qualified, messages


def format_briefing(qualified, messages):
    """Format the commercial briefing for CEO consumption."""
    
    lines = []
    lines.append("=" * 60)
    lines.append("📈 DAILY COMMERCIAL BRIEFING")
    lines.append("=" * 60)
    lines.append("")
    
    if not qualified:
        lines.append("⚠️  No qualified leads found today.")
        lines.append("   Check ICP criteria or expand search parameters.")
        return "\n".join(lines)
    
    lines.append(f"🎯 Found {len(qualified)} qualified prospects")
    lines.append("")
    
    # Summary table
    lines.append("QUALIFIED LEADS:")
    lines.append("-" * 60)
    for lead in qualified:
        score_indicator = "🔥" if lead["score"] >= 90 else "⭐" if lead["score"] >= 70 else "📍"
        lines.append(f"  {score_indicator} {lead['company']} | {lead['industry']} | {lead['city']} | {lead['employees']} emp | Score: {lead['score']}")
        if lead.get("reasons"):
            lines.append(f"      Reasons: {', '.join(lead['reasons'])}")
    lines.append("")
    
    # Outreach messages
    lines.append("OUTREACH MESSAGES:")
    lines.append("-" * 60)
    
    for msg in messages:
        lines.append(f"\n📬 {msg['company']}")
        lines.append(f"   Playbook: {msg['strategy']['playbook']}")
        lines.append(f"   Flow: {msg['strategy']['flow']} | Platform: {msg['strategy']['platform']} | Priority: {msg['strategy']['priority']}")
        lines.append(f"   ──────────────────")
        lines.append(f"   {msg['message']}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("NEXT ACTIONS:")
    lines.append("1. Review messages above")
    lines.append("2. Send via LinkedIn (Flow 1,2,5) or X/Twitter (Flow 4)")
    lines.append("3. Log sent messages in CRM")
    lines.append("4. Schedule follow-ups per playbook rules")
    lines.append("=" * 60)
    
    return "\n".join(lines)


if __name__ == "__main__":
    briefing, qualified, messages = run_commercial_briefing()
    print(briefing)