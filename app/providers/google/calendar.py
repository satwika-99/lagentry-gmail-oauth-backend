"""
Google Calendar API Implementation
Handles calendar operations, events, and scheduling
"""

import httpx
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import json

from ...core.database import db_manager
from ...core.exceptions import APIError, TokenError


class GoogleCalendarAPI:
    """Google Calendar API client for calendar operations"""
    
    def __init__(self):
        self.base_url = "https://www.googleapis.com/calendar/v3"
    
    async def _get_headers(self, user_email: str) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        tokens = db_manager.get_valid_tokens(user_email, "google")
        if not tokens:
            raise TokenError("No valid tokens found for user")
        
        return {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json"
        }
    
    async def list_calendars(self, user_email: str) -> Dict[str, Any]:
        """List all calendars for the user"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/users/me/calendarList", headers=headers)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to list calendars: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def get_calendar(self, user_email: str, calendar_id: str = "primary") -> Dict[str, Any]:
        """Get calendar details"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/calendars/{calendar_id}", headers=headers)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to get calendar: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def list_events(
        self, 
        user_email: str, 
        calendar_id: str = "primary",
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 50,
        single_events: bool = True,
        order_by: str = "startTime"
    ) -> Dict[str, Any]:
        """List events from a calendar"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "maxResults": max_results,
                "singleEvents": single_events,
                "orderBy": order_by
            }
            
            if time_min:
                params["timeMin"] = time_min.isoformat() + "Z"
            if time_max:
                params["timeMax"] = time_max.isoformat() + "Z"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/calendars/{calendar_id}/events",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to list events: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def get_event(
        self, 
        user_email: str, 
        event_id: str, 
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Get a specific event by ID"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/calendars/{calendar_id}/events/{event_id}",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to get event: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def create_event(
        self, 
        user_email: str, 
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Create a new calendar event"""
        try:
            headers = await self._get_headers(user_email)
            
            event = {
                "summary": summary,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "UTC"
                }
            }
            
            if description:
                event["description"] = description
            if location:
                event["location"] = location
            if attendees:
                event["attendees"] = [{"email": email} for email in attendees]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/calendars/{calendar_id}/events",
                    headers=headers,
                    json=event
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to create event: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def update_event(
        self, 
        user_email: str, 
        event_id: str,
        summary: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Update an existing calendar event"""
        try:
            headers = await self._get_headers(user_email)
            
            # Get current event first
            current_event = await self.get_event(user_email, event_id, calendar_id)
            
            # Update fields
            if summary:
                current_event["summary"] = summary
            if start_time:
                current_event["start"] = {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "UTC"
                }
            if end_time:
                current_event["end"] = {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "UTC"
                }
            if description:
                current_event["description"] = description
            if location:
                current_event["location"] = location
            if attendees:
                current_event["attendees"] = [{"email": email} for email in attendees]
            
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/calendars/{calendar_id}/events/{event_id}",
                    headers=headers,
                    json=current_event
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to update event: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def delete_event(
        self, 
        user_email: str, 
        event_id: str, 
        calendar_id: str = "primary"
    ) -> bool:
        """Delete a calendar event"""
        try:
            headers = await self._get_headers(user_email)
            
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/calendars/{calendar_id}/events/{event_id}",
                    headers=headers
                )
                response.raise_for_status()
                return True
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to delete event: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def search_events(
        self, 
        user_email: str, 
        query: str,
        calendar_id: str = "primary",
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """Search for events in a calendar"""
        try:
            headers = await self._get_headers(user_email)
            params = {
                "q": query,
                "maxResults": max_results
            }
            
            if time_min:
                params["timeMin"] = time_min.isoformat() + "Z"
            if time_max:
                params["timeMax"] = time_max.isoformat() + "Z"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/calendars/{calendar_id}/events",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to search events: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def get_free_busy(
        self, 
        user_email: str, 
        time_min: datetime,
        time_max: datetime,
        calendar_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get free/busy information for calendars"""
        try:
            headers = await self._get_headers(user_email)
            
            if not calendar_ids:
                calendar_ids = ["primary"]
            
            request_body = {
                "timeMin": time_min.isoformat() + "Z",
                "timeMax": time_max.isoformat() + "Z",
                "items": [{"id": cal_id} for cal_id in calendar_ids]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/freeBusy",
                    headers=headers,
                    json=request_body
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to get free/busy info: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")
    
    async def create_calendar(
        self, 
        user_email: str, 
        summary: str,
        description: Optional[str] = None,
        time_zone: str = "UTC"
    ) -> Dict[str, Any]:
        """Create a new calendar"""
        try:
            headers = await self._get_headers(user_email)
            
            calendar = {
                "summary": summary,
                "timeZone": time_zone
            }
            
            if description:
                calendar["description"] = description
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/calendars",
                    headers=headers,
                    json=calendar
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise APIError(f"Failed to create calendar: {e.response.text}")
        except Exception as e:
            raise APIError(f"Calendar API error: {str(e)}")


# API instance
calendar_api = GoogleCalendarAPI() 