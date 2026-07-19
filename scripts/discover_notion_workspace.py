#!/usr/bin/env python3
"""
Notion Workspace Discovery Script (Composio-first, Direct API fallback)

Discovers all existing pages and databases in the CraftedWorkflows Notion workspace.
Prefers Composio tool abstraction; falls back to direct Notion API if needed.

Usage:
    # Composio mode (preferred)
    export COMPOSIO_API_KEY=***
    python scripts/discover_notion_workspace.py

    # Direct API fallback mode
    export NOTION_API_KEY=***
    export NOTION_PARENT_PAGE_ID=xxx
    python scripts/discover_notion_workspace.py
"""

import os
import asyncio
import json
from typing import Dict, List, Any, Optional
from enum import Enum


class AuthMode(Enum):
    COMPOSIO = "composio"
    DIRECT_API = "direct_api"


def detect_auth_mode() -> tuple[AuthMode, Dict]:
    """Detect which authentication method is available."""
    composio_key = os.getenv("COMPOSIO_API_KEY")
    notion_key = os.getenv("NOTION_API_KEY")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    
    if composio_key:
        return AuthMode.COMPOSIO, {"api_key": composio_key}
    elif notion_key and parent_page_id:
        return AuthMode.DIRECT_API, {"api_key": notion_key, "parent_page_id": parent_page_id}
    else:
        raise RuntimeError(
            "No valid authentication found.\n"
            "Option 1 (Composio): export COMPOSIO_API_KEY=***\n"
            "Option 2 (Direct API): export NOTION_API_KEY=*** && export NOTION_PARENT_PAGE_ID=xxx"
        )


async def discover_via_composio(api_key: str) -> Dict:
    """Discover workspace via Composio tool abstraction."""
    try:
        from composio import Composio
    except ImportError:
        raise RuntimeError("composio package not installed. Install: pip install composio-core")
    
    client = Composio(api_key=api_key)
    tool_name = "notion"
    
    async def execute_action(action: str, params: Dict) -> Any:
        result = await client.tools.execute(
            tool_name=tool_name,
            action=action,
            params=params,
            entity_id="default"
        )
        return result
    
    # Search for accessible content
    print("1. Searching via Composio...")
    search_result = await execute_action("search", {"query": ""})
    all_results = search_result.get("results", []) if isinstance(search_result, dict) else []
    print(f"   Found {len(all_results)} total results")
    
    databases = []
    pages = []
    
    for result in all_results:
        if result.get("object") == "database":
            db_id = result["id"]
            try:
                db_data = await execute_action("get_database", {"database_id": db_id})
                title = extract_title(db_data)
                databases.append({
                    "id": db_id,
                    "title": title,
                    "url": f"https://notion.so/{db_id.replace('-', '')}",
                    "properties": db_data.get("properties", {}),
                    "created_time": db_data.get("created_time"),
                    "last_edited_time": db_data.get("last_edited_time"),
                })
                print(f"   📊 Database: {title} ({db_id})")
            except Exception as e:
                print(f"   Failed to get database {db_id}: {e}")
        elif result.get("object") == "page":
            page_id = result["id"]
            title = extract_title(result)
            pages.append({
                "id": page_id,
                "title": title,
                "url": f"https://notion.so/{page_id.replace('-', '')}",
            })
            print(f"   📄 Page: {title} ({page_id})")
    
    return {"databases": databases, "pages": pages, "mode": "composio"}


async def discover_via_direct_api(api_key: str, parent_page_id: str) -> Dict:
    """Discover workspace via direct Notion API (fallback)."""
    import aiohttp
    
    NOTION_VERSION = "2022-06-28"
    BASE_URL = "https://api.notion.com/v1"
    HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        print("1. Fetching parent page via Direct API...")
        parent = await get_page(session, HEADERS, BASE_URL, parent_page_id)
        parent_title = extract_title(parent)
        print(f"   Parent: {parent_title}")
        
        print("2. Fetching direct children...")
        children = await get_block_children(session, HEADERS, BASE_URL, parent_page_id)
        print(f"   Found {len(children)} direct children")
        
        databases = []
        pages = []
        
        for child in children:
            if child.get("type") == "child_database":
                db_id = child["id"]
                db_data = await get_database(session, HEADERS, BASE_URL, db_id)
                title = extract_title(db_data)
                databases.append({
                    "id": db_id,
                    "title": title,
                    "url": f"https://notion.so/{db_id.replace('-', '')}",
                    "properties": db_data.get("properties", {}),
                    "created_time": db_data.get("created_time"),
                    "last_edited_time": db_data.get("last_edited_time"),
                })
                print(f"   📊 Database: {title} ({db_id})")
            elif child.get("type") == "child_page":
                page_id = child["id"]
                page_data = await get_page(session, HEADERS, BASE_URL, page_id)
                title = extract_title(page_data)
                pages.append({
                    "id": page_id,
                    "title": title,
                    "url": f"https://notion.so/{page_id.replace('-', '')}",
                })
                print(f"   📄 Page: {title} ({page_id})")
        
        # Search for all accessible databases
        print("3. Searching all accessible content...")
        all_results = await search_all(session, HEADERS, BASE_URL)
        all_databases = [r for r in all_results if r.get("object") == "database"]
        all_pages = [r for r in all_results if r.get("object") == "page"]
        
        print(f"   Total databases found: {len(all_databases)}")
        print(f"   Total pages found: {len(all_pages)}")
        
        return {"databases": databases, "pages": pages, "mode": "direct_api"}


# Direct API helper functions
async def get_page(session, headers, base_url, page_id):
    async with session.get(f"{base_url}/pages/{page_id}", headers=headers) as resp:
        if resp.status >= 400:
            return {}
        return await resp.json()

async def get_block_children(session, headers, base_url, block_id):
    async with session.get(f"{base_url}/blocks/{block_id}/children", headers=headers, params={"page_size": 100}) as resp:
        if resp.status >= 400:
            return []
        return (await resp.json()).get("results", [])

async def get_database(session, headers, base_url, database_id):
    async with session.get(f"{base_url}/databases/{database_id}", headers=headers) as resp:
        if resp.status >= 400:
            return {}
        return await resp.json()

async def search_all(session, headers, base_url):
    async with session.post(f"{base_url}/search", headers=headers, json={"page_size": 100}) as resp:
        if resp.status >= 400:
            return []
        return (await resp.json()).get("results", [])

def extract_title(obj: Dict) -> str:
    if "title" in obj:
        title_array = obj["title"]
        if isinstance(title_array, list):
            return "".join([t.get("plain_text", "") for t in title_array])
        return str(title_array)
    if "properties" in obj and "Name" in obj["properties"]:
        name_prop = obj["properties"]["Name"]
        if name_prop.get("type") == "title":
            title_array = name_prop.get("title", [])
            return "".join([t.get("plain_text", "") for t in title_array])
    return "Untitled"


async def main():
    print("=" * 60)
    print("NOTION WORKSPACE DISCOVERY")
    print("=" * 60)
    
    # Detect auth mode
    try:
        mode, config = detect_auth_mode()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        exit(1)
    
    print(f"Mode: {mode.value}")
    
    if mode == AuthMode.COMPOSIO:
        result = await discover_via_composio(config["api_key"])
    else:
        result = await discover_via_direct_api(config["api_key"], config["parent_page_id"])
    
    databases = result["databases"]
    pages = result["pages"]
    mode_used = result["mode"]
    
    print()
    print(f"2. Summary ({mode_used}):")
    print(f"   Databases: {len(databases)}")
    print(f"   Pages: {len(pages)}")
    print()
    
    # Output detailed schema for each database
    print("3. Detailed database schemas:")
    print()
    
    for db in databases:
        print(f"--- {db['title']} ---")
        print(f"  ID: {db['id']}")
        print(f"  URL: {db['url']}")
        print(f"  Properties ({len(db['properties'])}):")
        for prop_name, prop_data in db['properties'].items():
            prop_type = prop_data.get("type", "unknown")
            if prop_type == "select":
                options = [o.get("name", "") for o in prop_data.get("select", {}).get("options", [])]
                print(f"    - {prop_name} ({prop_type}): {options}")
            elif prop_type == "multi_select":
                options = [o.get("name", "") for o in prop_data.get("multi_select", {}).get("options", [])]
                print(f"    - {prop_name} ({prop_type}): {options}")
            elif prop_type == "relation":
                rel_db = prop_data.get("relation", {}).get("database_id", "unknown")
                print(f"    - {prop_name} ({prop_type}): -> {rel_db}")
            else:
                print(f"    - {prop_name} ({prop_type})")
        print()
    
    # Save to file for analysis
    output = {
        "parent_page": {"title": "Discovered"} if mode == AuthMode.COMPOSIO else {},
        "databases": databases,
        "pages": pages,
        "discovery_mode": mode_used,
        "total_databases": len(databases),
        "total_pages": len(pages),
    }
    
    with open("notion_workspace_discovery.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print("=" * 60)
    print(f"Discovery complete ({mode_used}). Results saved to notion_workspace_discovery.json")
    print("=" * 60)


if __name__ == "__main__":
    import json
    asyncio.run(main())