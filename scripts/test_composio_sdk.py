#!/usr/bin/env python3
"""
Minimal Composio SDK v0.18 Test

Creates a Tool Router session, enables Notion toolkit, 
executes a simple Notion action, prints the result.
"""

import os
import sys

# Check if we have the API key
api_key = os.getenv("COMPOSIO_API_KEY")
if not api_key:
    print("ERROR: COMPOSIO_API_KEY not set")
    sys.exit(1)

print("=" * 60)
print("COMPOSIO SDK v0.18 MINIMAL TEST")
print("=" * 60)
print(f"API Key: {api_key[:10]}...")

try:
    from composio_client import Composio
    from composio_client.types import ToolExecuteParams
    print("✅ composio-client imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Initialize client
client = Composio(api_key=api_key)
print("✅ Composio client created")

# Test 1: List connected accounts
print("\n1. Testing connected_accounts.list()...")
try:
    accounts = client.connected_accounts.list()
    print(f"✅ Connected accounts: {len(accounts.items) if hasattr(accounts, 'items') else len(accounts)}")
    for acc in getattr(accounts, 'items', accounts):
        if hasattr(acc, 'toolkit_slug'):
            print(f"   - {acc.toolkit_slug} ({acc.status if hasattr(acc, 'status') else 'unknown'})")
except Exception as e:
    print(f"❌ connected_accounts.list() failed: {e}")

# Test 2: Create a session with Notion toolkit
print("\n2. Creating Tool Router session with Notion toolkit...")
try:
    # Get the Notion connected account
    accounts = client.connected_accounts.list()
    notion_account = None
    for acc in accounts.items:
        if hasattr(acc, 'toolkit') and acc.toolkit.slug == 'notion':
            notion_account = acc
            break
    
    if not notion_account:
        print("   No Notion connected account found")
        session_id = None
    else:
        session = client.tool_router.session.create(
            user_id=notion_account.user_id,
            connected_accounts={"notion": [notion_account.id]},
        )
        session_id = session.session_id
        print(f"✅ Session created: {session_id}")
        print(f"   Status: {session.status if hasattr(session, 'status') else 'N/A'}")
except Exception as e:
    print(f"❌ Session creation failed: {e}")
    session_id = None

# Test 3: Execute a simple Notion action
if session_id:
    print("\n3. Executing NOTION_SEARCH via tools.execute()...")
    try:
        result = client.tools.execute(
            tool_slug="NOTION_SEARCH",
            arguments={"query": ""},
            user_id="test_user",
        )
        
        # Convert response - new SDK uses .data attribute
        if hasattr(result, 'model_dump'):
            result_dict = result.model_dump()
        elif hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result
            
        print(f"✅ NOTION_SEARCH executed")
        print(f"   Response type: {type(result_dict)}")
        if isinstance(result_dict, dict):
            # New SDK: result.data contains the actual data
            if 'data' in result_dict and isinstance(result_dict['data'], dict):
                actual_data = result_dict['data']
                if 'results' in actual_data:
                    print(f"   Results count: {len(actual_data.get('results', []))}")
                else:
                    print(f"   Data keys: {list(actual_data.keys())}")
            elif 'results' in result_dict:
                print(f"   Results count: {len(result_dict.get('results', []))}")
            else:
                print(f"   Keys: {list(result_dict.keys())[:10]}")
        # Also print successful flag
        if hasattr(result, 'successful'):
            print(f"   Successful: {result.successful}")
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        import traceback
        traceback.print_exc()

# Test 4: Try getting a database (will fail if no databases, but tests the API)
if session_id:
    print("\n4. Testing NOTION_GET_DATABASE (expecting not found)...")
    try:
        result = client.tools.execute(
            tool_slug="NOTION_GET_DATABASE",
            arguments={"database_id": "test-id"},
            user_id="test_user",
        )
        print(f"✅ NOTION_GET_DATABASE executed (expected 404): {type(result)}")
        if hasattr(result, 'successful'):
            print(f"   Successful: {result.successful}")
    except Exception as e:
        print(f"   Expected error (no database): {type(e).__name__}")

print("\n" + "=" * 60)
print("MINIMAL TEST COMPLETE")
print("=" * 60)