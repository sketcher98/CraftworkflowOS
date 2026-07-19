"""
Notion CRM Database Schemas

Programmatic database schemas for creating Notion databases as CRM fallback
when HubSpot is unavailable. These schemas mirror HubSpot's object model
for seamless migration.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class NotionPropertyType(Enum):
    TITLE = "title"
    RICH_TEXT = "rich_text"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    CHECKBOX = "checkbox"
    URL = "url"
    RELATION = "relation"
    PEOPLE = "people"
    FILES = "files"
    CREATED_TIME = "created_time"
    LAST_EDITED_TIME = "last_edited_time"


class SelectOption:
    def __init__(self, name: str, color: str = "default"):
        self.name = name
        self.color = color

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "color": self.color}


@dataclass
class NotionProperty:
    name: str
    type: NotionPropertyType
    options: List[SelectOption] = field(default_factory=list)
    relation_database_id: Optional[str] = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        prop = {"type": self.type.value}
        
        if self.type in [NotionPropertyType.SELECT, NotionPropertyType.MULTI_SELECT]:
            prop[self.type.value] = {
                "options": [opt.to_dict() for opt in self.options]
            }
        
        if self.type == NotionPropertyType.RELATION:
            prop["relation"] = {
                "database_id": self.relation_database_id,
                "single_property": {}
            }
        
        if self.description:
            prop["description"] = self.description
            
        return {self.name: prop}


# ============================================================================
# DATABASE SCHEMAS
# ============================================================================

LEADS_SCHEMA = [
    NotionProperty("Lead ID", NotionPropertyType.TITLE, description="Auto-generated: LD-{timestamp}"),
    NotionProperty("Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Email", NotionPropertyType.EMAIL),
    NotionProperty("Phone", NotionPropertyType.PHONE_NUMBER),
    NotionProperty("Company", NotionPropertyType.RELATION, description="Relation to Companies DB"),
    NotionProperty("Source", NotionPropertyType.SELECT, options=[
        SelectOption("Inbound", "green"),
        SelectOption("Outbound", "blue"),
        SelectOption("Referral", "purple"),
        SelectOption("Event", "orange"),
        SelectOption("Organic", "gray"),
    ]),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("New", "blue"),
        SelectOption("Qualified", "green"),
        SelectOption("Contacted", "yellow"),
        SelectOption("Disqualified", "red"),
        SelectOption("Converted", "purple"),
    ]),
    NotionProperty("Score", NotionPropertyType.NUMBER, description="0-100"),
    NotionProperty("ICP Tier", NotionPropertyType.SELECT, options=[
        SelectOption("Tier 1", "green"),
        SelectOption("Tier 2", "blue"),
        SelectOption("Tier 3", "gray"),
    ]),
    NotionProperty("Assigned To", NotionPropertyType.PEOPLE),
    NotionProperty("Created Date", NotionPropertyType.CREATED_TIME),
    NotionProperty("Last Contact", NotionPropertyType.DATE),
    NotionProperty("Next Action", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
    NotionProperty("HubSpot ID", NotionPropertyType.RICH_TEXT, description="For future migration"),
]

COMPANIES_SCHEMA = [
    NotionProperty("Company ID", NotionPropertyType.TITLE, description="Auto-generated: CO-{timestamp}"),
    NotionProperty("Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Domain", NotionPropertyType.URL),
    NotionProperty("Industry", NotionPropertyType.SELECT, options=[
        SelectOption("Agency", "blue"),
        SelectOption("Consultancy", "green"),
        SelectOption("SaaS", "purple"),
        SelectOption("E-commerce", "orange"),
        SelectOption("Other", "gray"),
    ]),
    NotionProperty("Size", NotionPropertyType.SELECT, options=[
        SelectOption("1-10", "gray"),
        SelectOption("11-50", "blue"),
        SelectOption("51-200", "green"),
        SelectOption("201-500", "yellow"),
        SelectOption("500+", "red"),
    ]),
    NotionProperty("Location", NotionPropertyType.RICH_TEXT),
    NotionProperty("Annual Revenue", NotionPropertyType.NUMBER),
    NotionProperty("Website", NotionPropertyType.URL),
    NotionProperty("LinkedIn", NotionPropertyType.URL),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Prospect", "blue"),
        SelectOption("Lead", "yellow"),
        SelectOption("Customer", "green"),
        SelectOption("Churned", "red"),
    ]),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("Created Date", NotionPropertyType.CREATED_TIME),
    NotionProperty("Last Updated", NotionPropertyType.LAST_EDITED_TIME),
    NotionProperty("HubSpot ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

CONTACTS_SCHEMA = [
    NotionProperty("Contact ID", NotionPropertyType.TITLE, description="Auto-generated: CT-{timestamp}"),
    NotionProperty("First Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Last Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Email", NotionPropertyType.EMAIL),
    NotionProperty("Phone", NotionPropertyType.PHONE_NUMBER),
    NotionProperty("Title", NotionPropertyType.RICH_TEXT),
    NotionProperty("Company", NotionPropertyType.RELATION),
    NotionProperty("Lead", NotionPropertyType.RELATION),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Active", "green"),
        SelectOption("Inactive", "gray"),
        SelectOption("Do Not Contact", "red"),
    ]),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("Created Date", NotionPropertyType.CREATED_TIME),
    NotionProperty("Last Contact", NotionPropertyType.DATE),
    NotionProperty("HubSpot ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

OPPORTUNITIES_SCHEMA = [
    NotionProperty("Opportunity ID", NotionPropertyType.TITLE, description="Auto-generated: OP-{timestamp}"),
    NotionProperty("Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Company", NotionPropertyType.RELATION),
    NotionProperty("Contact", NotionPropertyType.RELATION),
    NotionProperty("Lead", NotionPropertyType.RELATION),
    NotionProperty("Stage", NotionPropertyType.SELECT, options=[
        SelectOption("Discovery", "blue"),
        SelectOption("Qualification", "purple"),
        SelectOption("Proposal", "yellow"),
        SelectOption("Negotiation", "orange"),
        SelectOption("Closed Won", "green"),
        SelectOption("Closed Lost", "red"),
    ]),
    NotionProperty("Amount", NotionPropertyType.NUMBER),
    NotionProperty("Probability", NotionPropertyType.NUMBER, description="0-100%"),
    NotionProperty("Expected Close Date", NotionPropertyType.DATE),
    NotionProperty("Actual Close Date", NotionPropertyType.DATE),
    NotionProperty("Product", NotionPropertyType.SELECT, options=[
        SelectOption("Jumpstart", "blue"),
        SelectOption("Goldilocks", "green"),
        SelectOption("Visionary", "purple"),
        SelectOption("Custom", "gray"),
    ]),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("Created Date", NotionPropertyType.CREATED_TIME),
    NotionProperty("Last Updated", NotionPropertyType.LAST_EDITED_TIME),
    NotionProperty("HubSpot Deal ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

SALES_CALLS_SCHEMA = [
    NotionProperty("Call ID", NotionPropertyType.TITLE, description="Auto-generated: SC-{timestamp}"),
    NotionProperty("Date", NotionPropertyType.DATE),
    NotionProperty("Time", NotionPropertyType.RICH_TEXT),
    NotionProperty("Duration", NotionPropertyType.NUMBER, description="Minutes"),
    NotionProperty("Type", NotionPropertyType.SELECT, options=[
        SelectOption("Discovery", "blue"),
        SelectOption("Demo", "purple"),
        SelectOption("Proposal Review", "yellow"),
        SelectOption("Negotiation", "orange"),
        SelectOption("Follow-up", "blue"),
        SelectOption("QBR", "purple"),
    ]),
    NotionProperty("Lead", NotionPropertyType.RELATION),
    NotionProperty("Contact", NotionPropertyType.RELATION),
    NotionProperty("Company", NotionPropertyType.RELATION),
    NotionProperty("Opportunity", NotionPropertyType.RELATION),
    NotionProperty("Outcome", NotionPropertyType.SELECT, options=[
        SelectOption("Scheduled", "blue"),
        SelectOption("Completed", "green"),
        SelectOption("No Show", "red"),
        SelectOption("Cancelled", "gray"),
        SelectOption("Rescheduled", "orange"),
    ]),
    NotionProperty("Recording URL", NotionPropertyType.URL),
    NotionProperty("Transcript", NotionPropertyType.RICH_TEXT),
    NotionProperty("Key Insights", NotionPropertyType.RICH_TEXT),
    NotionProperty("Action Items", NotionPropertyType.RICH_TEXT),
    NotionProperty("Next Steps", NotionPropertyType.RICH_TEXT),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("HubSpot Activity ID", NotionPropertyType.RICH_TEXT),
]

PROPOSALS_SCHEMA = [
    NotionProperty("Proposal ID", NotionPropertyType.TITLE, description="Auto-generated: PR-{timestamp}"),
    NotionProperty("Title", NotionPropertyType.RICH_TEXT),
    NotionProperty("Opportunity", NotionPropertyType.RELATION),
    NotionProperty("Company", NotionPropertyType.RELATION),
    NotionProperty("Contact", NotionPropertyType.RELATION),
    NotionProperty("Stage", NotionPropertyType.SELECT, options=[
        SelectOption("Draft", "gray"),
        SelectOption("Sent", "blue"),
        SelectOption("Viewed", "purple"),
        SelectOption("Negotiating", "orange"),
        SelectOption("Accepted", "green"),
        SelectOption("Rejected", "red"),
        SelectOption("Expired", "gray"),
    ]),
    NotionProperty("Tier", NotionPropertyType.SELECT, options=[
        SelectOption("Jumpstart", "blue"),
        SelectOption("Goldilocks", "green"),
        SelectOption("Visionary", "purple"),
        SelectOption("Custom", "gray"),
    ]),
    NotionProperty("Amount", NotionPropertyType.NUMBER),
    NotionProperty("Sent Date", NotionPropertyType.DATE),
    NotionProperty("Viewed Date", NotionPropertyType.DATE),
    NotionProperty("Response Date", NotionPropertyType.DATE),
    NotionProperty("Expiry Date", NotionPropertyType.DATE),
    NotionProperty("Document URL", NotionPropertyType.URL),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("HubSpot Deal ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

CLIENTS_SCHEMA = [
    NotionProperty("Client ID", NotionPropertyType.TITLE, description="Auto-generated: CL-{timestamp}"),
    NotionProperty("Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Company", NotionPropertyType.RELATION),
    NotionProperty("Primary Contact", NotionPropertyType.RELATION),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Onboarding", "blue"),
        SelectOption("Active", "green"),
        SelectOption("At Risk", "orange"),
        SelectOption("Churned", "red"),
        SelectOption("Alumni", "gray"),
    ]),
    NotionProperty("Tier", NotionPropertyType.SELECT, options=[
        SelectOption("Jumpstart", "blue"),
        SelectOption("Goldilocks", "green"),
        SelectOption("Visionary", "purple"),
        SelectOption("Custom", "gray"),
    ]),
    NotionProperty("Monthly Value", NotionPropertyType.NUMBER),
    NotionProperty("Contract Start", NotionPropertyType.DATE),
    NotionProperty("Contract End", NotionPropertyType.DATE),
    NotionProperty("Renewal Date", NotionPropertyType.DATE),
    NotionProperty("Health Score", NotionPropertyType.NUMBER, description="0-100"),
    NotionProperty("CSM", NotionPropertyType.PEOPLE),
    NotionProperty("HubSpot Company ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

PROJECTS_SCHEMA = [
    NotionProperty("Project ID", NotionPropertyType.TITLE, description="Auto-generated: PJ-{timestamp}"),
    NotionProperty("Name", NotionPropertyType.RICH_TEXT),
    NotionProperty("Client", NotionPropertyType.RELATION),
    NotionProperty("Type", NotionPropertyType.SELECT, options=[
        SelectOption("Implementation", "blue"),
        SelectOption("Optimization", "green"),
        SelectOption("Migration", "purple"),
        SelectOption("Support", "orange"),
        SelectOption("Custom", "gray"),
    ]),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Planning", "blue"),
        SelectOption("Active", "green"),
        SelectOption("On Hold", "orange"),
        SelectOption("Completed", "green"),
        SelectOption("Cancelled", "red"),
    ]),
    NotionProperty("Progress", NotionPropertyType.NUMBER, description="0-100%"),
    NotionProperty("Start Date", NotionPropertyType.DATE),
    NotionProperty("Target End Date", NotionPropertyType.DATE),
    NotionProperty("Actual End Date", NotionPropertyType.DATE),
    NotionProperty("Budget", NotionPropertyType.NUMBER),
    NotionProperty("Spent", NotionPropertyType.NUMBER),
    NotionProperty("PM", NotionPropertyType.PEOPLE),
    NotionProperty("Team", NotionPropertyType.PEOPLE),
    NotionProperty("HubSpot Project ID", NotionPropertyType.RICH_TEXT),
    NotionProperty("Notes", NotionPropertyType.RICH_TEXT),
]

TASKS_SCHEMA = [
    NotionProperty("Task ID", NotionPropertyType.TITLE, description="Auto-generated: TK-{timestamp}"),
    NotionProperty("Title", NotionPropertyType.RICH_TEXT),
    NotionProperty("Description", NotionPropertyType.RICH_TEXT),
    NotionProperty("Project", NotionPropertyType.RELATION),
    NotionProperty("Client", NotionPropertyType.RELATION),
    NotionProperty("Assignee", NotionPropertyType.PEOPLE),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Backlog", "gray"),
        SelectOption("Ready", "blue"),
        SelectOption("In Progress", "yellow"),
        SelectOption("Review", "purple"),
        SelectOption("Done", "green"),
        SelectOption("Blocked", "red"),
    ]),
    NotionProperty("Priority", NotionPropertyType.SELECT, options=[
        SelectOption("Low", "gray"),
        SelectOption("Medium", "blue"),
        SelectOption("High", "orange"),
        SelectOption("Critical", "red"),
    ]),
    NotionProperty("Due Date", NotionPropertyType.DATE),
    NotionProperty("Estimated Hours", NotionPropertyType.NUMBER),
    NotionProperty("Actual Hours", NotionPropertyType.NUMBER),
    NotionProperty("Sprint", NotionPropertyType.RICH_TEXT),
    NotionProperty("Tags", NotionPropertyType.MULTI_SELECT),
    NotionProperty("Created Date", NotionPropertyType.CREATED_TIME),
    NotionProperty("Completed Date", NotionPropertyType.DATE),
    NotionProperty("HubSpot Task ID", NotionPropertyType.RICH_TEXT),
]

SOPS_SCHEMA = [
    NotionProperty("SOP ID", NotionPropertyType.TITLE, description="Auto-generated: SOP-{timestamp}"),
    NotionProperty("Title", NotionPropertyType.RICH_TEXT),
    NotionProperty("Category", NotionPropertyType.SELECT, options=[
        SelectOption("Sales", "blue"),
        SelectOption("Marketing", "purple"),
        SelectOption("Delivery", "green"),
        SelectOption("Operations", "orange"),
        SelectOption("Finance", "yellow"),
        SelectOption("HR", "pink"),
        SelectOption("Technical", "gray"),
    ]),
    NotionProperty("Status", NotionPropertyType.SELECT, options=[
        SelectOption("Draft", "gray"),
        SelectOption("Review", "yellow"),
        SelectOption("Approved", "green"),
        SelectOption("Published", "blue"),
        SelectOption("Archived", "red"),
    ]),
    NotionProperty("Version", NotionPropertyType.NUMBER),
    NotionProperty("Owner", NotionPropertyType.PEOPLE),
    NotionProperty("Reviewer", NotionPropertyType.PEOPLE),
    NotionProperty("Approved By", NotionPropertyType.PEOPLE),
    NotionProperty("Approved Date", NotionPropertyType.DATE),
    NotionProperty("Review Date", NotionPropertyType.DATE),
    NotionProperty("Document URL", NotionPropertyType.URL),
    NotionProperty("Tags", NotionPropertyType.MULTI_SELECT),
    NotionProperty("Applies To", NotionPropertyType.MULTI_SELECT, options=[
        SelectOption("Leads", "blue"),
        SelectOption("Companies", "green"),
        SelectOption("Contacts", "purple"),
        SelectOption("Opportunities", "yellow"),
        SelectOption("Clients", "green"),
        SelectOption("Projects", "blue"),
    ]),
    NotionProperty("HubSpot ID", NotionPropertyType.RICH_TEXT),
]


# ============================================================================
# MASTER SCHEMA REGISTRY
# ============================================================================

ALL_SCHEMAS = {
    "Leads": LEADS_SCHEMA,
    "Companies": COMPANIES_SCHEMA,
    "Contacts": CONTACTS_SCHEMA,
    "Opportunities": OPPORTUNITIES_SCHEMA,
    "Sales Calls": SALES_CALLS_SCHEMA,
    "Proposals": PROPOSALS_SCHEMA,
    "Clients": CLIENTS_SCHEMA,
    "Projects": PROJECTS_SCHEMA,
    "Tasks": TASKS_SCHEMA,
    "SOPs": SOPS_SCHEMA,
}


def generate_notion_create_payload(database_name: str, parent_page_id: str, schema: List[NotionProperty]) -> Dict[str, Any]:
    """Generate Notion API payload for creating a database."""
    properties = {}
    for prop in schema:
        properties.update(prop.to_dict())
    
    return {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": database_name}}],
        "properties": properties,
    }


def get_all_schemas() -> Dict[str, List[NotionProperty]]:
    """Return all database schemas."""
    return ALL_SCHEMAS.copy()


def get_schema(database_name: str) -> List[NotionProperty]:
    """Get schema for specific database."""
    return ALL_SCHEMAS.get(database_name, [])


if __name__ == "__main__":
    # Print all schemas for verification
    for name, schema in ALL_SCHEMAS.items():
        print(f"\n=== {name} ===")
        for prop in schema:
            print(f"  - {prop.name} ({prop.type.value})")
            if prop.options:
                print(f"    Options: {[o.name for o in prop.options]}")
            if prop.relation_database_id:
                print(f"    Relation: {prop.relation_database_id}")