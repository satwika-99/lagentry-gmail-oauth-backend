# Example agent registry/config for connectors
CONNECTORS = {
    # ... existing connectors ...
    "microsoft": {
        "name": "Microsoft",
        "services": ["outlook", "onedrive", "calendar"],
        "auth_url": "/api/v1/microsoft/auth-url",
        "callback_url": "/api/v1/microsoft/callback",
        "endpoints": {
            "outlook_emails": "/api/v1/microsoft/outlook/emails",
            "onedrive_files": "/api/v1/microsoft/onedrive/files",
            "calendar_events": "/api/v1/microsoft/calendar/events"
        },
        "description": "Access Outlook Mail, OneDrive Files, and Calendar via Microsoft Graph."
    },
    "notion": {
        "name": "Notion",
        "services": ["databases", "pages", "search", "blocks"],
        "auth_url": "/api/v1/notion/auth-url",
        "callback_url": "/api/v1/notion/callback",
        "endpoints": {
            "search_databases": "/api/v1/notion/databases",
            "get_database": "/api/v1/notion/databases/{database_id}",
            "query_database": "/api/v1/notion/databases/{database_id}/query",
            "search_pages": "/api/v1/notion/pages",
            "get_page": "/api/v1/notion/pages/{page_id}",
            "get_page_content": "/api/v1/notion/pages/{page_id}/content",
            "create_page": "/api/v1/notion/pages",
            "update_page": "/api/v1/notion/pages/{page_id}",
            "delete_page": "/api/v1/notion/pages/{page_id}",
            "get_user": "/api/v1/notion/user"
        },
        "description": "Access Notion databases, pages, and content via Notion API."
    }
}
