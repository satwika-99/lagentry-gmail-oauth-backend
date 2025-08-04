"""
Connectors package initialization
Registers all available connectors with the factory
"""

from .base import ConnectorFactory
from .google.gmail_connector import GmailConnector
from .slack.slack_connector import SlackConnector
from .atlassian.jira_connector import JiraConnector

# Register all connectors
ConnectorFactory.register("gmail", GmailConnector)
ConnectorFactory.register("slack", SlackConnector)
ConnectorFactory.register("jira", JiraConnector)

__all__ = [
    "ConnectorFactory",
    "GmailConnector", 
    "SlackConnector",
    "JiraConnector"
]
