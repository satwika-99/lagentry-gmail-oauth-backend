"""
Connectors package initialization
Registers all available connectors with the factory
"""

from .base import ConnectorFactory
from .google.gmail_connector import GmailConnector
from .slack.slack_connector import SlackConnector
from .atlassian.jira_connector import JiraConnector
from .atlassian.confluence_connector import ConfluenceConnector

# Register all connectors
ConnectorFactory.register("gmail", GmailConnector)
ConnectorFactory.register("slack", SlackConnector)
ConnectorFactory.register("jira", JiraConnector)
ConnectorFactory.register("atlassian", JiraConnector)  # Also register as atlassian for API compatibility
ConnectorFactory.register("confluence", ConfluenceConnector)  # Confluence connector

__all__ = [
    "ConnectorFactory",
    "GmailConnector", 
    "SlackConnector",
    "JiraConnector"
]
