# Tool Router Specification

Canonical interface for routing tool/external service calls through Composio and direct integrations.

---

## Tool Abstraction Principle

Employees request **capabilities**, never specific tools. The Tool Router maps capability → tool → integration.

---

## Tool Categories

### 1. Composio-Managed Tools (OAuth/App-based)

```python
COMPOSIO_TOOLS = {
    "hubspot": {
        "capabilities": ["crm"],
        "actions": [
            "create_contact", "update_contact", "get_contact",
            "create_deal", "update_deal", "get_deal",
            "create_company", "get_company",
            "search_contacts", "search_deals",
            "create_note", "log_activity"
        ],
        "auth": "oauth",
        "scopes": ["crm.objects.contacts.read", "crm.objects.contacts.write", 
                   "crm.objects.deals.read", "crm.objects.deals.write"],
        "rate_limit": 100
    },
    "gmail": {
        "capabilities": ["email"],
        "actions": [
            "send_email", "get_email", "search_emails",
            "create_draft", "get_thread",
            "add_label", "create_label"
        ],
        "auth": "oauth",
        "scopes": ["https://www.googleapis.com/auth/gmail.send",
                   "https://www.googleapis.com/auth/gmail.readonly"],
        "rate_limit": 250
    },
    "notion": {
        "capabilities": ["document"],
        "actions": [
            "create_page", "update_page", "get_page",
            "query_database", "create_database",
            "append_block", "get_block_children"
        ],
        "auth": "oauth",
        "scopes": ["read", "write"],
        "rate_limit": 100
    },
    "google_docs": {
        "capabilities": ["document"],
        "actions": [
            "create_document", "update_document", "get_document",
            "create_from_template", "export_pdf"
        ],
        "auth": "oauth",
        "scopes": ["https://www.googleapis.com/auth/documents"],
        "rate_limit": 100
    },
    "google_sheets": {
        "capabilities": ["spreadsheet"],
        "actions": [
            "create_spreadsheet", "read_range", "write_range",
            "append_rows", "get_sheet", "create_sheet"
        ],
        "auth": "oauth",
        "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
        "rate_limit": 100
    },
    "google_calendar": {
        "capabilities": ["calendar"],
        "actions": [
            "create_event", "get_event", "update_event", "delete_event",
            "list_events", "get_free_busy", "create_calendar"
        ],
        "auth": "oauth",
        "scopes": ["https://www.googleapis.com/auth/calendar"],
        "rate_limit": 500
    },
    "slack": {
        "capabilities": ["communication"],
        "actions": [
            "send_message", "send_dm", "create_channel",
            "invite_to_channel", "get_channel_history",
            "upload_file", "add_reaction"
        ],
        "auth": "oauth",
        "scopes": ["chat:write", "channels:read", "groups:read", 
                   "im:write", "files:write"],
        "rate_limit": 100
    },
    "telegram": {
        "capabilities": ["communication"],
        "actions": [
            "send_message", "send_photo", "send_document",
            "create_group", "get_chat", "pin_message"
        ],
        "auth": "bot_token",
        "scopes": [],
        "rate_limit": 30
    },
    "make": {
        "capabilities": ["automation"],
        "actions": [
            "run_scenario", "get_scenario", "list_scenarios",
            "create_webhook", "get_execution_log"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "figma": {
        "capabilities": ["design"],
        "actions": [
            "get_file", "get_nodes", "get_images",
            "post_comment", "get_comments"
        ],
        "auth": "personal_token",
        "scopes": [],
        "rate_limit": 300
    },
    "perplexity": {
        "capabilities": ["research"],
        "actions": ["search", "deep_research"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 60
    },
    "exa": {
        "capabilities": ["search"],
        "actions": ["search", "deep_research", "crawl"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 50
    },
    "calendly": {
        "capabilities": ["calendar"],
        "actions": [
            "get_event_types", "get_scheduled_events",
            "create_webhook", "get_user"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "typefully": {
        "capabilities": ["social_posting"],
        "actions": [
            "create_draft", "publish_draft", "schedule_draft",
            "get_analytics", "get_account"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 50
    },
    "google_super": {
        "capabilities": ["search", "drive", "calendar", "gmail", "docs", "sheets"],
        "actions": ["unified_google_operations"],
        "auth": "oauth",
        "scopes": ["https://www.googleapis.com/auth/drive",
                   "https://www.googleapis.com/auth/calendar",
                   "https://www.googleapis.com/auth/gmail.send"],
        "rate_limit": 100
    },
    "dropbox": {
        "capabilities": ["storage"],
        "actions": [
            "upload_file", "download_file", "create_folder",
            "list_folder", "share_file", "get_link"
        ],
        "auth": "oauth",
        "scopes": ["files.content.read", "files.content.write"],
        "rate_limit": 100
    },
    "cloudinary": {
        "capabilities": ["storage", "image_transform"],
        "actions": [
            "upload_image", "transform_image", "delete_image",
            "get_image_info", "list_images"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 500
    },
    "tinypng": {
        "capabilities": ["image_compress"],
        "actions": ["compress_image"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 500
    },
    "giphy": {
        "capabilities": ["gif_search"],
        "actions": ["search_gifs", "get_gif", "trending"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "html_to_image": {
        "capabilities": ["html_render"],
        "actions": ["render_html_to_image"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 50
    },
    "imgbb": {
        "capabilities": ["image_hosting"],
        "actions": ["upload_image", "delete_image"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "tally_forms": {
        "capabilities": ["form"],
        "actions": ["create_form", "get_submissions", "get_form"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 50
    },
    "lemonsqueezy": {
        "capabilities": ["payment"],
        "actions": [
            "create_product", "create_checkout", "get_order",
            "list_products", "create_subscription"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "gumroad": {
        "capabilities": ["payment"],
        "actions": [
            "create_product", "get_sales", "get_product",
            "create_license"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "canva": {
        "capabilities": ["design"],
        "actions": [
            "create_design", "get_design", "export_design",
            "get_templates", "upload_media"
        ],
        "auth": "oauth",
        "scopes": ["design:read", "design:write"],
        "rate_limit": 60
    },
    "vapi": {
        "capabilities": ["voice_ai"],
        "actions": [
            "create_assistant", "start_call", "get_call",
            "end_call", "get_transcript"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 30
    },
    "groqcloud": {
        "capabilities": ["writing", "analysis", "coding"],
        "actions": ["chat_completion"],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 30
    },
    "paystack": {
        "capabilities": ["payment"],
        "actions": [
            "initialize_transaction", "verify_transaction",
            "create_customer", "create_plan", "charge_customer"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 200
    },
    "supabase": {
        "capabilities": ["database", "auth", "storage", "realtime"],
        "actions": [
            "query", "insert", "update", "delete",
            "rpc", "subscribe", "upload_file"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 100
    },
    "daytona": {
        "capabilities": ["sandbox"],
        "actions": [
            "create_sandbox", "execute_code", "get_logs",
            "install_package", "destroy_sandbox"
        ],
        "auth": "api_key",
        "scopes": [],
        "rate_limit": 20
    },
    "facebook": {
        "capabilities": ["social_posting", "ads"],
        "actions": [
            "create_post", "create_ad", "get_insights",
            "get_page", "create_campaign"
        ],
        "auth": "oauth",
        "scopes": ["pages_manage_posts", "ads_management"],
        "rate_limit": 200
    }
}
```

### 2. Direct API Integrations (Non-Composio)

```python
DIRECT_TOOLS = {
    "github": {
        "capabilities": ["code_hosting", "ci_cd"],
        "actions": [
            "create_repo", "create_pr", "merge_pr",
            "get_workflow_run", "trigger_workflow",
            "get_file", "create_file", "update_file"
        ],
        "auth": "pat",
        "endpoint": "https://api.github.com",
        "rate_limit": 5000
    },
    "gitlab": {
        "capabilities": ["code_hosting", "ci_cd"],
        "actions": ["create_project", "create_mr", "trigger_pipeline"],
        "auth": "pat",
        "endpoint": "https://gitlab.com/api/v4",
        "rate_limit": 600
    },
    "linear": {
        "capabilities": ["project_management"],
        "actions": [
            "create_issue", "update_issue", "get_issue",
            "create_project", "get_team", "search_issues"
        ],
        "auth": "api_key",
        "endpoint": "https://api.linear.app/graphql",
        "rate_limit": 100
    },
    "jira": {
        "capabilities": ["project_management"],
        "actions": [
            "create_issue", "transition_issue", "search_issues",
            "add_comment", "get_sprint", "create_sprint"
        ],
        "auth": "basic_or_token",
        "endpoint": "https://{domain}.atlassian.net/rest/api/3",
        "rate_limit": 100
    },
    "asana": {
        "capabilities": ["project_management"],
        "actions": [
            "create_task", "update_task", "get_task",
            "create_project", "get_project", "search_tasks"
        ],
        "auth": "pat",
        "endpoint": "https://app.asana.com/api/1.0",
        "rate_limit": 100
    },
    "monday": {
        "capabilities": ["project_management"],
        "actions": [
            "create_item", "update_item", "get_items",
            "create_board", "get_board"
        ],
        "auth": "api_key",
        "endpoint": "https://api.monday.com/v2",
        "rate_limit": 60
    },
    "zendesk": {
        "capabilities": ["support"],
        "actions": [
            "create_ticket", "update_ticket", "get_ticket",
            "search_tickets", "add_comment", "get_user"
        ],
        "auth": "api_token",
        "endpoint": "https://{subdomain}.zendesk.com/api/v2",
        "rate_limit": 700
    },
    "intercom": {
        "capabilities": ["support", "messaging"],
        "actions": [
            "create_conversation", "reply_to_conversation",
            "get_contact", "tag_contact", "create_event"
        ],
        "auth": "pat",
        "endpoint": "https://api.intercom.io",
        "rate_limit": 100
    },
    "stripe": {
        "capabilities": ["payment"],
        "actions": [
            "create_payment_intent", "create_customer",
            "create_subscription", "create_invoice",
            "get_payment_method", "create_refund"
        ],
        "auth": "secret_key",
        "endpoint": "https://api.stripe.com/v1",
        "rate_limit": 100
    },
    "quickbooks": {
        "capabilities": ["accounting"],
        "actions": [
            "create_invoice", "get_invoice", "create_customer",
            "get_report", "create_journal_entry"
        ],
        "auth": "oauth",
        "endpoint": "https://quickbooks.api.intuit.com/v3",
        "rate_limit": 50
    },
    "xero": {
        "capabilities": ["accounting"],
        "actions": [
            "create_invoice", "get_invoice", "create_contact",
            "get_report", "create_bank_transaction"
        ],
        "auth": "oauth",
        "endpoint": "https://api.xero.com/api.xro/2.0",
        "rate_limit": 60
    },
    "sendgrid": {
        "capabilities": ["email"],
        "actions": [
            "send_email", "create_template", "get_stats",
            "add_contact", "create_list"
        ],
        "auth": "api_key",
        "endpoint": "https://api.sendgrid.com/v3",
        "rate_limit": 600
    },
    "mailgun": {
        "capabilities": ["email"],
        "actions": [
            "send_email", "get_events", "create_template",
            "add_domain", "verify_domain"
        ],
        "auth": "api_key",
        "endpoint": "https://api.mailgun.net/v3",
        "rate_limit": 300
    },
    "postmark": {
        "capabilities": ["email"],
        "actions": [
            "send_email", "get_message", "get_stats",
            "create_template", "get_suppressions"
        ],
        "auth": "server_token",
        "endpoint": "https://api.postmarkapp.com",
        "rate_limit": 300
    },
    "twilio": {
        "capabilities": ["sms", "voice", "whatsapp"],
        "actions": [
            "send_sms", "make_call", "send_whatsapp",
            "get_message_status", "create_messaging_service"
        ],
        "auth": "account_sid+auth_token",
        "endpoint": "https://api.twilio.com/2010-04-01",
        "rate_limit": 100
    },
    "vercel": {
        "capabilities": ["deployment"],
        "actions": [
            "create_deployment", "get_deployment",
            "list_deployments", "create_project",
            "get_logs", "rollback"
        ],
        "auth": "token",
        "endpoint": "https://api.vercel.com",
        "rate_limit": 60
    },
    "netlify": {
        "capabilities": ["deployment"],
        "actions": [
            "create_deploy", "get_deploy", "list_sites",
            "create_site", "get_site", "unlock_deploy"
        ],
        "auth": "pat",
        "endpoint": "https://api.netlify.com/api/v1",
        "rate_limit": 60
    },
    "aws": {
        "capabilities": ["cloud"],
        "actions": [
            "lambda_invoke", "s3_upload", "s3_download",
            "dynamodb_query", "sns_publish", "sqs_send",
            "ecs_run_task", "cloudformation_deploy"
        ],
        "auth": "aws_credentials",
        "endpoint": "various",
        "rate_limit": 1000
    },
    "gcp": {
        "capabilities": ["cloud"],
        "actions": [
            "cloud_function_deploy", "cloud_run_deploy",
            "bigquery_query", "pubsub_publish", "storage_upload"
        ],
        "auth": "service_account",
        "endpoint": "various",
        "rate_limit": 1000
    },
    "cloudflare": {
        "capabilities": ["cdn", "dns", "workers"],
        "actions": [
            "purge_cache", "create_dns_record", "update_dns",
            "deploy_worker", "get_analytics"
        ],
        "auth": "api_token",
        "endpoint": "https://api.cloudflare.com/client/v4",
        "rate_limit": 1200
    },
    "datadog": {
        "capabilities": ["monitoring"],
        "actions": [
            "create_dashboard", "get_metrics", "create_monitor",
            "get_logs", "create_slo"
        ],
        "auth": "api_key+app_key",
        "endpoint": "https://api.datadoghq.com/api/v1",
        "rate_limit": 600
    },
    "grafana": {
        "capabilities": ["monitoring", "visualization"],
        "actions": [
            "create_dashboard", "get_dashboard", "query_prometheus",
            "create_alert", "get_alerts"
        ],
        "auth": "api_key",
        "endpoint": "https://{instance}.grafana.net/api",
        "rate_limit": 100
    },
    "sentry": {
        "capabilities": ["error_tracking"],
        "actions": [
            "get_issues", "get_issue", "resolve_issue",
            "create_release", "get_events"
        ],
        "auth": "auth_token",
        "endpoint": "https://sentry.io/api/0",
        "rate_limit": 100
    },
    "pagerduty": {
        "capabilities": ["incident_management"],
        "actions": [
            "create_incident", "get_incident", "acknowledge_incident",
            "resolve_incident", "get_on_call", "create_service"
        ],
        "auth": "api_key",
        "endpoint": "https://api.pagerduty.com",
        "rate_limit": 100
    }
}
```

---

## Tool Router Interface

```python
def execute_tool(capability: str, action: str, params: dict, context: RuntimeContext = None) -> ToolResult:
    """
    Execute a tool action for a capability.
    
    Args:
        capability: Canonical capability (e.g., "crm", "email", "automation")
        action: Specific action (e.g., "create_contact", "send_email")
        params: Action parameters
        context: Runtime context for routing
        
    Returns:
        ToolResult with output, metadata, and status
    """
    
    # 1. Find tool for capability
    tool = find_tool_for_capability(capability)
    if not tool:
        raise ToolNotFoundError(f"No tool for capability: {capability}")
    
    # 2. Verify action exists
    if action not in tool["actions"]:
        raise ActionNotFoundError(f"Action '{action}' not in tool '{tool['name']}'")
    
    # 3. Check auth
    if not verify_auth(tool):
        raise AuthError(f"Auth not configured for {tool['name']}")
    
    # 4. Execute via appropriate executor
    if tool["category"] == "composio":
        return execute_composio(tool, action, params)
    elif tool["category"] == "direct":
        return execute_direct_api(tool, action, params)
    else:
        raise ToolExecutorError(f"Unknown tool category: {tool['category']}")


def execute_composio(tool: dict, action: str, params: dict) -> ToolResult:
    """Execute via Composio SDK."""
    from composio import Composio
    
    client = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    connected_account = get_connected_account(tool["name"])
    
    if not connected_account:
        raise AuthError(f"No connected account for {tool['name']}")
    
    result = client.execute(
        app=tool["name"],
        action=action,
        params=params,
        connected_account_id=connected_account.id
    )
    
    return ToolResult(
        success=True,
        output=result,
        tool=tool["name"],
        action=action,
        latency_ms=result.latency_ms
    )


def execute_direct_api(tool: dict, action: str, params: dict) -> ToolResult:
    """Execute via direct API call."""
    import requests
    
    endpoint = f"{tool['endpoint']}/{ACTION_ENDPOINTS[tool['name']][action]}"
    headers = build_auth_headers(tool)
    
    response = requests.request(
        method=ACTION_METHODS[tool["name"]][action],
        url=endpoint,
        headers=headers,
        json=params,
        timeout=30
    )
    
    if response.status_code >= 400:
        raise ToolExecutionError(f"{tool['name']} {action} failed: {response.text}")
    
    return ToolResult(
        success=True,
        output=response.json(),
        tool=tool["name"],
        action=action,
        latency_ms=response.elapsed.total_seconds() * 1000
    )
```

---

## ToolResult Schema

```json
{
  "success": true,
  "tool": "hubspot",
  "action": "create_contact",
  "output": {"contact_id": "12345", "email": "test@example.com"},
  "latency_ms": 342,
  "metadata": {
    "rate_limit_remaining": 98,
    "api_version": "v3"
  },
  "errors": []
}
```

---

## Error Handling

```python
class ToolError(Exception):
    pass

class ToolNotFoundError(ToolError):
    pass

class ActionNotFoundError(ToolError):
    pass

class AuthError(ToolError):
    pass

class ToolExecutionError(ToolError):
    pass

class RateLimitError(ToolError):
    pass

# Retry logic
def execute_with_retry(executor, *args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return executor(*args, **kwargs)
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except ToolExecutionError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    raise MaxRetriesExceededError()
```

---

## Integration Pattern

```python
# Employee uses capability router
result = request("crm", "Create contact for new lead", {
    "email": "founder@agency.com",
    "properties": {"company": "AgencyCo", "tier": "Goldilocks"}
})

# Internally:
# 1. Capability router maps "crm" → Provider Router
# 2. Provider Router selects "HubSpot" (healthy, lowest cost)
# 3. Tool Router executes "hubspot.create_contact" via Composio
# 4. Result returned as CapabilityResult with ToolResult embedded
```

---

## Configuration

```yaml
# config/tools.yaml
tools:
  hubspot:
    category: "composio"
    enabled: true
    default: true
  salesforce:
    category: "direct"
    enabled: false
    endpoint: "https://mycompany.salesforce.com"
    
oauth:
  hubspot:
    client_id: "${HUBSPOT_CLIENT_ID}"
    client_secret: "${HUBSPOT_CLIENT_SECRET}"
    redirect_uri: "https://app.craftedworkflows.com/oauth/callback"
```

---

## Testing Requirements

```python
def test_tool_router():
    # Test capability -> tool mapping
    for cap in ["crm", "email", "automation", "document", "calendar"]:
        tool = find_tool_for_capability(cap)
        assert tool is not None
    
    # Test action existence
    tool = find_tool_for_capability("crm")
    assert "create_contact" in tool["actions"]
    
    # Test auth verification
    assert verify_auth(tool) == True  # if configured
    
    # Test execution (mock)
    with mock_composio():
        result = execute_tool("crm", "create_contact", {"email": "test@test.com"})
        assert result.success == True
        assert "contact_id" in result.output
    
    # Test error handling
    with mock_composio_error(401):
        try:
            execute_tool("crm", "create_contact", {"email": "test@test.com"})
            assert False
        except AuthError:
            pass
```