#!/usr/bin/env python3
"""
Notion Workspace Discovery Script

Discovers all existing pages and databases in the CraftedWorkflows Notion workspace.
Run this AFTER setting NOTION_API_KEY and NOTION_PARENT_PAGE_ID environment variables.

Usage:
    export NOTION_API_KEY=secret_xxx
    export NOTION_PARENT_PAGE_ID=xxx
    python scripts/discover_notion_workspace.py
"""

import os
import asyncio
import json
from typing import Dict, List, Any, Optional
import aiohttp

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY environment variable not set")
    exit(1)

if not PARENT_PAGE_ID:
    print("ERROR: NOTION_PARENT_PAGE_ID environment variable not set")
    exit(1)

NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


async def search_all(session: aiohttp.ClientSession) -> List[Dict]:
    """Search for all pages and databases accessible to the integration."""
    url = f"{BASE_URL}/search"
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {
            "page_size": 100,
        }
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        async with session.post(url, headers=HEADERS, json=payload) as resp:
            if resp.status >= 400:
                error = await resp.text()
                raise RuntimeError(f"Notion API error: {error}")
            data = await resp.json()
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
    
    return all_results


async def get_block_children(session: aiohttp.ClientSession, block_id: str) -> List[Dict]:
    """Get all children of a block (page/database)."""
    url = f"{BASE_URL}/blocks/{block_id}/children"
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        params = {"page_size": 100}
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        async with session.get(url, headers=HEADERS, params=params) as resp:
            if resp.status >= 400:
                return []
            data = await resp.json()
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
    
    return all_results


async def get_database(session: aiohttp.ClientSession, database_id: str) -> Dict:
    """Get full database schema."""
    url = f"{BASE_URL}/databases/{database_id}"
    async with session.get(url, headers=HEADERS) as resp:
        if resp.status >= 400:
            return {}
        return await resp.json()


async def get_page(session: aiohttp.ClientSession, page_id: str) -> Dict:
    """Get page details."""
    url = f"{BASE_URL}/pages/{page_id}"
    async with session.get(url, headers=HEADERS) as resp:
        if resp.status >= 400:
            return {}
        return await resp.json()


def extract_title(obj: Dict) -> str:
    """Extract title from page or database object."""
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
    print(f"Parent Page ID: {PARENT_PAGE_ID}")
    print()
    
    async with aiohttp.ClientSession() as session:
        # First, get the parent page to understand structure
        print("1. Fetching parent page...")
        parent = await get_page(session, PARENT_PAGE_ID)
        parent_title = extract_title(parent)
        print(f"   Parent: {parent_title}")
        print()
        
        # Get all children of parent page
        print("2. Fetching direct children of parent page...")
        children = await get_block_children(session, PARENT_PAGE_ID)
        print(f"   Found {len(children)} direct children")
        
        databases = []
        pages = []
        
        for child in children:
            if child.get("type") == "child_database":
                db_id = child["id"]
                db_data = await get_database(session, db_id)
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
                page_data = await get_page(session, page_id)
                title = extract_title(page_data)
                pages.append({
                    "id": page_id,
                    "title": title,
                    "url": f"https://notion.so/{page_id.replace('-', '')}",
                })
                print(f"   📄 Page: {title} ({page_id})")
        
        print()
        print(f"3. Summary:")
        print(f"   Databases: {len(databases)}")
        print(f"   Pages: {len(pages)}")
        print()
        
        # Search for all accessible databases (not just direct children)
        print("4. Searching all accessible databases...")
        all_results = await search_all(session)
        all_databases = [r for r in all_results if r.get("object") == "database"]
        all_pages = [r for r in all_results if r.get("object") == "page"]
        
        print(f"   Total databases found: {len(all_databases)}")
        print(f"   Total pages found: {len(all_pages)}")
        print()
        
        # Output detailed schema for each database
        print("5. Detailed database schemas:")
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
            "parent_page": {"id": PARENT_PAGE_ID, "title": parent_title},
            "direct_children": {
                "databases": databases,
                "pages": pages,
            },
            "all_accessible": {
                "databases": len(all_databases),
                "pages": len(all_pages),
            }
        }
        
        with open("notion_workspace_discovery.json", "w") as f:
            json.dump(output, f, indent=2, default=str)
        
        print("=" * 60)
        print("Discovery complete. Results saved to notion_workspace_discovery.json")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())