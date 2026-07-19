"""
Notion CRM Client

CRM operations using Notion as the primary backend (HubSpot fallback).
All operations degrade gracefully to Notion when HubSpot is unavailable.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from runtime.notion_crm_schemas import (
    ALL_SCHEMAS,
    get_schema,
    generate_notion_create_payload,
)

logger = logging.getLogger(__name__)


class CRMProvider(Enum):
    NOTION = "notion"
    HUBSPOT = "hubspot"


@dataclass
class CRMConfig:
    """CRM configuration with provider preference."""
    primary_provider: CRMProvider = CRMProvider.NOTION
    fallback_provider: CRMProvider = CRMProvider.NOTION
    hubspot_available: bool = False
    
    # Notion database IDs (set after database creation)
    leads_db_id: Optional[str] = None
    companies_db_id: Optional[str] = None
    contacts_db_id: Optional[str] = None
    opportunities_db_id: Optional[str] = None
    sales_calls_db_id: Optional[str] = None
    proposals_db_id: Optional[str] = None
    clients_db_id: Optional[str] = None
    projects_db_id: Optional[str] = None
    tasks_db_id: Optional[str] = None
    sops_db_id: Optional[str] = None
    
    # Parent page ID for database creation
    parent_page_id: Optional[str] = None


class NotionCRMClient:
    """
    Notion-based CRM client for CraftworkflowOS.
    Serves as primary CRM when HubSpot is unavailable.
    """
    
    def __init__(self, config: CRMConfig):
        self.config = config
        self.composio_api_key = os.getenv("COMPOSIO_API_KEY")
        self.notion_token = os.getenv("NOTION_API_KEY")
        
        if not self.notion_token:
            logger.warning("NOTION_API_KEY not set - Notion CRM will not function")
    
    def _get_db_id(self, db_name: str) -> Optional[str]:
        """Get database ID by name."""
        attr = f"{db_name.lower().replace(' ', '_')}_db_id"
        return getattr(self.config, attr, None)
    
    def _set_db_id(self, db_name: str, db_id: str):
        """Set database ID by name."""
        attr = f"{db_name.lower().replace(' ', '_')}_db_id"
        setattr(self.config, attr, db_id)
    
    async def create_all_databases(self, parent_page_id: str) -> Dict[str, str]:
        """Create all CRM databases in Notion."""
        from runtime.notion_crm_schemas import get_all_schemas, generate_notion_create_payload
        
        self.config.parent_page_id = parent_page_id
        created_dbs = {}
        
        for db_name, schema in ALL_SCHEMAS.items():
            try:
                payload = generate_notion_create_payload(db_name, parent_page_id, schema)
                db_id = await self._create_database(payload)
                self._set_db_id(db_name, db_id)
                created_dbs[db_name] = db_id
                logger.info(f"Created database: {db_name} ({db_id})")
            except Exception as e:
                logger.error(f"Failed to create {db_name}: {e}")
        
        return created_dbs
    
    async def _create_database(self, payload: Dict) -> str:
        """Create a single database via Notion API."""
        if not self.notion_token:
            raise RuntimeError("NOTION_API_KEY not configured")
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/databases",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as resp:
                if resp.status >= 400:
                    error = await resp.text()
                    raise RuntimeError(f"Notion API error: {error}")
                data = await resp.json()
                return data["id"]
    
    # ========================================================================
    # LEAD OPERATIONS
    # ========================================================================
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in Notion."""
        db_id = self._get_db_id("Leads")
        if not db_id:
            raise RuntimeError("Leads database not initialized")
        
        # Ensure Lead ID is auto-generated
        lead_data.setdefault("Lead ID", f"LD-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        lead_data.setdefault("Created Date", datetime.now().isoformat())
        
        return await self._create_page("Leads", db_id, lead_data)
    
    async def get_lead(self, lead_id: str) -> Optional[Dict]:
        """Get lead by Notion page ID."""
        return await self._get_page(lead_id)
    
    async def search_leads(self, filters: Dict[str, Any]) -> List[Dict]:
        """Search leads with filters."""
        db_id = self._get_db_id("Leads")
        if not db_id:
            return []
        
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_lead(self, lead_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a lead."""
        return await self._update_page(lead_id, updates)
    
    async def delete_lead(self, lead_id: str) -> bool:
        """Archive a lead (soft delete)."""
        return await self._archive_page(lead_id)
    
    # ========================================================================
    # COMPANY OPERATIONS
    # ========================================================================
    
    async def create_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new company."""
        db_id = self._get_db_id("Companies")
        if not db_id:
            raise RuntimeError("Companies database not initialized")
        
        company_data.setdefault("Company ID", f"CO-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        company_data.setdefault("Created Date", datetime.now().isoformat())
        
        return await self._create_page("Companies", db_id, company_data)
    
    async def get_company(self, company_id: str) -> Optional[Dict]:
        return await self._get_page(company_id)
    
    async def search_companies(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Companies")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_company(self, company_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        return await self._update_page(company_id, updates)
    
    # ========================================================================
    # CONTACT OPERATIONS
    # ========================================================================
    
    async def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Contacts")
        if not db_id:
            raise RuntimeError("Contacts database not initialized")
        
        contact_data.setdefault("Contact ID", f"CT-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        contact_data.setdefault("Created Date", datetime.now().isoformat())
        
        return await self._create_page("Contacts", db_id, contact_data)
    
    async def get_contact(self, contact_id: str) -> Optional[Dict]:
        return await self._get_page(contact_id)
    
    async def search_contacts(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Contacts")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        return await self._update_page(contact_id, updates)
    
    # ========================================================================
    # OPPORTUNITY OPERATIONS
    # ========================================================================
    
    async def create_opportunity(self, opp_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Opportunities")
        if not db_id:
            raise RuntimeError("Opportunities database not initialized")
        
        opp_data.setdefault("Opportunity ID", f"OP-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        opp_data.setdefault("Created Date", datetime.now().isoformat())
        
        return await self._create_page("Opportunities", db_id, opp_data)
    
    async def get_opportunity(self, opp_id: str) -> Optional[Dict]:
        return await self._get_page(opp_id)
    
    async def search_opportunities(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Opportunities")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_opportunity(self, opp_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        return await self._update_page(opp_id, updates)
    
    async def update_opportunity_stage(self, opp_id: str, stage: str) -> Dict[str, Any]:
        """Update opportunity stage with validation."""
        valid_stages = ["Discovery", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
        if stage not in valid_stages:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {valid_stages}")
        
        updates = {"Stage": stage}
        if stage == "Closed Won":
            updates["Actual Close Date"] = datetime.now().isoformat()
        
        return await self._update_page(opp_id, updates)
    
    # ========================================================================
    # SALES CALL OPERATIONS
    # ========================================================================
    
    async def create_sales_call(self, call_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Sales Calls")
        if not db_id:
            raise RuntimeError("Sales Calls database not initialized")
        
        call_data.setdefault("Call ID", f"SC-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        return await self._create_page("Sales Calls", db_id, call_data)
    
    async def get_sales_call(self, call_id: str) -> Optional[Dict]:
        return await self._get_page(call_id)
    
    async def search_sales_calls(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Sales Calls")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    # ========================================================================
    # PROPOSAL OPERATIONS
    # ========================================================================
    
    async def create_proposal(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Proposals")
        if not db_id:
            raise RuntimeError("Proposals database not initialized")
        
        proposal_data.setdefault("Proposal ID", f"PR-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        proposal_data.setdefault("Sent Date", datetime.now().isoformat())
        
        return await self._create_page("Proposals", db_id, proposal_data)
    
    async def get_proposal(self, proposal_id: str) -> Optional[Dict]:
        return await self._get_page(proposal_id)
    
    async def search_proposals(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Proposals")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_proposal_stage(self, proposal_id: str, stage: str) -> Dict[str, Any]:
        valid_stages = ["Draft", "Sent", "Viewed", "Negotiating", "Accepted", "Rejected", "Expired"]
        if stage not in valid_stages:
            raise ValueError(f"Invalid stage: {stage}")
        
        updates = {"Stage": stage}
        if stage in ["Accepted", "Rejected"]:
            updates["Response Date"] = datetime.now().isoformat()
        
        return await self._update_page(proposal_id, updates)
    
    # ========================================================================
    # CLIENT OPERATIONS
    # ========================================================================
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Clients")
        if not db_id:
            raise RuntimeError("Clients database not initialized")
        
        client_data.setdefault("Client ID", f"CL-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        return await self._create_page("Clients", db_id, client_data)
    
    async def get_client(self, client_id: str) -> Optional[Dict]:
        return await self._get_page(client_id)
    
    async def search_clients(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Clients")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_client_health(self, client_id: str, health_score: int) -> Dict[str, Any]:
        if not 0 <= health_score <= 100:
            raise ValueError("Health score must be 0-100")
        return await self._update_page(client_id, {"Health Score": health_score})
    
    # ========================================================================
    # PROJECT OPERATIONS
    # ========================================================================
    
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Projects")
        if not db_id:
            raise RuntimeError("Projects database not initialized")
        
        project_data.setdefault("Project ID", f"PJ-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        return await self._create_page("Projects", db_id, project_data)
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        return await self._get_page(project_id)
    
    async def search_projects(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Projects")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_project_progress(self, project_id: str, progress: int) -> Dict[str, Any]:
        if not 0 <= progress <= 100:
            raise ValueError("Progress must be 0-100")
        return await self._update_page(project_id, {"Progress": progress})
    
    # ========================================================================
    # TASK OPERATIONS
    # ========================================================================
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("Tasks")
        if not db_id:
            raise RuntimeError("Tasks database not initialized")
        
        task_data.setdefault("Task ID", f"TK-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        task_data.setdefault("Created Date", datetime.now().isoformat())
        
        return await self._create_page("Tasks", db_id, task_data)
    
    async def get_task(self, task_id: str) -> Optional[Dict]:
        return await self._get_page(task_id)
    
    async def search_tasks(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("Tasks")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    async def update_task_status(self, task_id: str, status: str) -> Dict[str, Any]:
        valid_statuses = ["Backlog", "Ready", "In Progress", "Review", "Done", "Blocked"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")
        
        updates = {"Status": status}
        if status == "Done":
            updates["Completed Date"] = datetime.now().isoformat()
        
        return await self._update_page(task_id, updates)
    
    # ========================================================================
    # SOP OPERATIONS
    # ========================================================================
    
    async def create_sop(self, sop_data: Dict[str, Any]) -> Dict[str, Any]:
        db_id = self._get_db_id("SOPs")
        if not db_id:
            raise RuntimeError("SOPs database not initialized")
        
        sop_data.setdefault("SOP ID", f"SOP-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        return await self._create_page("SOPs", db_id, sop_data)
    
    async def get_sop(self, sop_id: str) -> Optional[Dict]:
        return await self._get_page(sop_id)
    
    async def search_sops(self, filters: Dict[str, Any]) -> List[Dict]:
        db_id = self._get_db_id("SOPs")
        if not db_id:
            return []
        filter_conditions = self._build_filters(filters)
        return await self._query_database(db_id, filter_conditions)
    
    # ========================================================================
    # INTERNAL HELPERS
    # ========================================================================
    
    def _build_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build Notion API filter conditions."""
        if not filters:
            return {}
        
        conditions = []
        for key, value in filters.items():
            if isinstance(value, dict):
                # Complex filter: {"property": {"operator": "value"}}
                conditions.append({"property": key, **value})
            elif isinstance(value, list):
                # Multi-select or list filter
                conditions.append({"property": key, "multi_select": {"contains": value[0]}})
            else:
                # Exact match
                conditions.append({"property": key, "rich_text": {"equals": str(value)}})
        
        if len(conditions) == 1:
            return conditions[0]
        return {"and": conditions}
    
    async def _create_page(self, db_name: str, db_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a page in a Notion database."""
        if not self.notion_token:
            raise RuntimeError("NOTION_API_KEY not configured")
        
        # Transform data to Notion properties format
        properties = self._transform_to_notion_properties(db_name, data)
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={
                    "parent": {"database_id": db_id},
                    "properties": properties,
                },
            ) as resp:
                if resp.status >= 400:
                    error = await resp.text()
                    raise RuntimeError(f"Notion API error: {error}")
                return await resp.json()
    
    async def _get_page(self, page_id: str) -> Optional[Dict]:
        """Get a page by ID."""
        if not self.notion_token:
            return None
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                },
            ) as resp:
                if resp.status == 404:
                    return None
                if resp.status >= 400:
                    return None
                return await resp.json()
    
    async def _update_page(self, page_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a page."""
        if not self.notion_token:
            raise RuntimeError("NOTION_API_KEY not configured")
        
        properties = self._transform_to_notion_properties("Generic", data)
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={"properties": properties},
            ) as resp:
                if resp.status >= 400:
                    error = await resp.text()
                    raise RuntimeError(f"Notion API error: {error}")
                return await resp.json()
    
    async def _archive_page(self, page_id: str) -> bool:
        """Archive (soft delete) a page."""
        if not self.notion_token:
            return False
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={"archived": True},
            ) as resp:
                return resp.status < 400
    
    async def _query_database(self, db_id: str, filter_conditions: Dict) -> List[Dict]:
        """Query a Notion database with filters."""
        if not self.notion_token:
            return []
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://api.notion.com/v1/databases/{db_id}/query",
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={"filter": filter_conditions} if filter_conditions else {},
            ) as resp:
                if resp.status >= 400:
                    return []
                data = await resp.json()
                return data.get("results", [])
    
    def _transform_to_notion_properties(self, db_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform plain data dict to Notion properties format."""
        properties = {}
        
        for key, value in data.items():
            if value is None:
                continue
            
            # Simple type mapping
            if isinstance(value, str):
                if key.lower().endswith("id") or key.lower().endswith("id"):
                    properties[key] = {"title": [{"text": {"content": value}}]}
                elif "@" in value and "." in value:
                    properties[key] = {"email": value}
                elif value.startswith("http"):
                    properties[key] = {"url": value}
                else:
                    properties[key] = {"rich_text": [{"text": {"content": value}}]}
            elif isinstance(value, (int, float)):
                properties[key] = {"number": value}
            elif isinstance(value, bool):
                properties[key] = {"checkbox": value}
            elif isinstance(value, datetime):
                properties[key] = {"date": {"start": value.isoformat()}}
            elif isinstance(value, list):
                # Multi-select
                properties[key] = {"multi_select": [{"name": v} for v in value if v]}
            elif isinstance(value, dict):
                # Relation or complex object
                if "id" in value:
                    properties[key] = {"relation": [{"id": value["id"]}]}
        
        return properties


# ============================================================================
# CRM MANAGER - High-level CRM operations
# ============================================================================

class CRMManager:
    """
    High-level CRM manager that handles provider selection and degradation.
    """
    
    def __init__(self, config: CRMConfig):
        self.config = config
        self.notion_client = NotionCRMClient(config)
        self.hubspot_available = config.hubspot_available
    
    @property
    def active_provider(self) -> CRMProvider:
        if self.hubspot_available:
            return CRMProvider.HUBSPOT
        return CRMProvider.NOTION
    
    async def initialize(self, parent_page_id: str) -> Dict[str, str]:
        """Initialize all Notion databases."""
        return await self.notion_client.create_all_databases(parent_page_id)
    
    def set_hubspot_available(self, available: bool):
        """Update HubSpot availability."""
        self.hubspot_available = available
        logger.info(f"HubSpot availability: {available}")
    
    def get_crm_status(self) -> Dict[str, Any]:
        """Get CRM system status."""
        return {
            "active_provider": self.active_provider.value,
            "hubspot_available": self.hubspot_available,
            "notion_configured": bool(self.notion_client.notion_token),
            "databases_initialized": {
                "Leads": bool(self.notion_client._get_db_id("Leads")),
                "Companies": bool(self.notion_client._get_db_id("Companies")),
                "Contacts": bool(self.notion_client._get_db_id("Contacts")),
                "Opportunities": bool(self.notion_client._get_db_id("Opportunities")),
                "Sales Calls": bool(self.notion_client._get_db_id("Sales Calls")),
                "Proposals": bool(self.notion_client._get_db_id("Proposals")),
                "Clients": bool(self.notion_client._get_db_id("Clients")),
                "Projects": bool(self.notion_client._get_db_id("Projects")),
                "Tasks": bool(self.notion_client._get_db_id("Tasks")),
                "SOPs": bool(self.notion_client._get_db_id("SOPs")),
            }
        }
    
    # Delegate all operations to Notion client
    async def create_lead(self, data: Dict) -> Dict:
        return await self.notion_client.create_lead(data)
    
    async def get_lead(self, lead_id: str) -> Optional[Dict]:
        return await self.notion_client.get_lead(lead_id)
    
    async def search_leads(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_leads(filters)
    
    async def update_lead(self, lead_id: str, updates: Dict) -> Dict:
        return await self.notion_client.update_lead(lead_id, updates)
    
    async def create_company(self, data: Dict) -> Dict:
        return await self.notion_client.create_company(data)
    
    async def get_company(self, company_id: str) -> Optional[Dict]:
        return await self.notion_client.get_company(company_id)
    
    async def search_companies(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_companies(filters)
    
    async def update_company(self, company_id: str, updates: Dict) -> Dict:
        return await self.notion_client.update_company(company_id, updates)
    
    async def create_contact(self, data: Dict) -> Dict:
        return await self.notion_client.create_contact(data)
    
    async def get_contact(self, contact_id: str) -> Optional[Dict]:
        return await self.notion_client.get_contact(contact_id)
    
    async def search_contacts(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_contacts(filters)
    
    async def update_contact(self, contact_id: str, updates: Dict) -> Dict:
        return await self.notion_client.update_contact(contact_id, updates)
    
    async def create_opportunity(self, data: Dict) -> Dict:
        return await self.notion_client.create_opportunity(data)
    
    async def get_opportunity(self, opp_id: str) -> Optional[Dict]:
        return await self.notion_client.get_opportunity(opp_id)
    
    async def search_opportunities(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_opportunities(filters)
    
    async def update_opportunity(self, opp_id: str, updates: Dict) -> Dict:
        return await self.notion_client.update_opportunity(opp_id, updates)
    
    async def update_opportunity_stage(self, opp_id: str, stage: str) -> Dict:
        return await self.notion_client.update_opportunity_stage(opp_id, stage)
    
    async def create_sales_call(self, data: Dict) -> Dict:
        return await self.notion_client.create_sales_call(data)
    
    async def get_sales_call(self, call_id: str) -> Optional[Dict]:
        return await self.notion_client.get_sales_call(call_id)
    
    async def search_sales_calls(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_sales_calls(filters)
    
    async def create_proposal(self, data: Dict) -> Dict:
        return await self.notion_client.create_proposal(data)
    
    async def get_proposal(self, proposal_id: str) -> Optional[Dict]:
        return await self.notion_client.get_proposal(proposal_id)
    
    async def search_proposals(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_proposals(filters)
    
    async def update_proposal_stage(self, proposal_id: str, stage: str) -> Dict:
        return await self.notion_client.update_proposal_stage(proposal_id, stage)
    
    async def create_client(self, data: Dict) -> Dict:
        return await self.notion_client.create_client(data)
    
    async def get_client(self, client_id: str) -> Optional[Dict]:
        return await self.notion_client.get_client(client_id)
    
    async def search_clients(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_clients(filters)
    
    async def update_client_health(self, client_id: str, health_score: int) -> Dict:
        return await self.notion_client.update_client_health(client_id, health_score)
    
    async def create_project(self, data: Dict) -> Dict:
        return await self.notion_client.create_project(data)
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        return await self.notion_client.get_project(project_id)
    
    async def search_projects(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_projects(filters)
    
    async def update_project_progress(self, project_id: str, progress: int) -> Dict:
        return await self.notion_client.update_project_progress(project_id, progress)
    
    async def create_task(self, data: Dict) -> Dict:
        return await self.notion_client.create_task(data)
    
    async def get_task(self, task_id: str) -> Optional[Dict]:
        return await self.notion_client.get_task(task_id)
    
    async def search_tasks(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_tasks(filters)
    
    async def update_task_status(self, task_id: str, status: str) -> Dict:
        return await self.notion_client.update_task_status(task_id, status)
    
    async def create_sop(self, data: Dict) -> Dict:
        return await self.notion_client.create_sop(data)
    
    async def get_sop(self, sop_id: str) -> Optional[Dict]:
        return await self.notion_client.get_sop(sop_id)
    
    async def search_sops(self, filters: Dict) -> List[Dict]:
        return await self.notion_client.search_sops(filters)


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_crm_manager(
    parent_page_id: str,
    hubspot_available: bool = False,
) -> CRMManager:
    """Create and initialize CRM manager."""
    config = CRMConfig(
        primary_provider=CRMProvider.NOTION,
        hubspot_available=hubspot_available,
        parent_page_id=parent_page_id,
    )
    
    manager = CRMManager(config)
    return manager


def create_notion_crm_client(config: CRMConfig = None) -> NotionCRMClient:
    """Create Notion CRM client with default config."""
    if config is None:
        config = CRMConfig()
    return NotionCRMClient(config)