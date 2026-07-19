#!/usr/bin/env python3
"""
Notion Database Initialization Script

Creates all 12 CRM databases in Notion for CraftworkflowOS.
Run this once after setting up Notion integration and getting API credentials.

Usage:
    export NOTION_API_KEY=secret_xxx
    export NOTION_PARENT_PAGE_ID=xxx
    python scripts/init_notion_databases.py
"""

import os
import asyncio
import logging
from typing import Dict

from runtime.notion_crm_schemas import ALL_SCHEMAS, generate_notion_create_payload
from runtime.notion_crm_client import create_crm_manager, CRMConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_notion_databases():
    """Initialize all CRM databases in Notion."""
    
    notion_token = os.getenv("NOTION_API_KEY")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    
    if not notion_token:
        raise RuntimeError("NOTION_API_KEY environment variable not set")
    if not parent_page_id:
        raise RuntimeError("NOTION_PARENT_PAGE_ID environment variable not set")
    
    logger.info("Creating CRM manager...")
    config = CRMConfig(
        primary_provider="notion",
        hubspot_available=False,
        parent_page_id=parent_page_id,
    )
    manager = create_crm_manager(config)
    
    logger.info(f"Creating 12 databases under parent page: {parent_page_id}")
    
    try:
        created_dbs = await manager.initialize(parent_page_id)
        
        logger.info("=" * 60)
        logger.info("DATABASE CREATION COMPLETE")
        logger.info("=" * 60)
        for name, db_id in created_dbs.items():
            logger.info(f"  {name}: {db_id}")
        
        logger.info("")
        logger.info("NEXT STEPS:")
        logger.info("1. Copy the database IDs above to your environment variables:")
        for name, db_id in created_dbs.items():
            env_var = f"NOTION_{name.upper().replace(' ', '_').replace('-', '_')}_DB_ID"
            logger.info(f"   export {env_var}={db_id}")
        
        logger.info("")
        logger.info("2. Verify databases in Notion UI")
        logger.info("3. Run workflow integration tests")
        
        return created_dbs
        
    except Exception as e:
        logger.error(f"Failed to create databases: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_notion_databases())