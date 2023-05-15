###############################################################################
#
#  Google Calendar API. This is a wrapper around the Google Calendar API.     
#
#  Author: W. P. Hooten
#  Date: 15-MAY-2023
#  For: Special Victims Mentor
#
###############################################################################

import datetime
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

###############################################################################

###############################################################################
# Google Calendar API

class GoogleCalendarAPI:
   
    ###########################################################################   
    # Initialize the Google Calendar API

    def __init__(self, credentials):
        
        self.calendar_service = build('calendar', 'v3', credentials=credentials)

    ###########################################################################

    ###########################################################################
    # Create a new event on a calendar

    def create_event(self, calendar_id):
        calendar_id = 'gmail@woodyhooten.com'
        event_summary = 'Example Event'
        event_description = 'This is an example event. Created using the Google Calendar API in Python. 4pm!'
        start_time = datetime.datetime.utcnow()
        end_time = start_time + datetime.timedelta(hours=1)
        event = {
            'summary': event_summary,
            'description': event_description,
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'UTC',
                },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'UTC',
            },
        }
        event = self.calendar_service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        # return response.json()

    ###########################################################################

    ###########################################################################
    # Create a new calendar

    def create_calendar(self, calendar_name):
        calendar_exists = False
        calendars = self.load_calendars()
        for calendar in calendars:
            if calendar['summary'] == calendar_name:
                calendar_exists = True
                print('Calendar already exists')
                break
        
        if not calendar_exists:
            calendar = {
                "summary": calendar_name,
                "timeZone": "America/New_York",
                "description": "A calendar created for 4pm."
            }
            
            new_calendar = self.calendar_service.calendars().insert(body=calendar).execute()
            rule = {
                "scope": {
                    "type": "user",
                    "value": "frymatic@woodyhooten.com"
                },
                "role": "writer"
            }
            try:
                self.calendar_service.acl().insert(calendarId=new_calendar['id'], body=rule).execute()
                
            except HttpError as error:
                if error.resp.status == 403:
                    error_details = error._get_reason().split("\n")[0]  # Get the first line of the error message
                    if "cannotChangeOwnAcl" in error_details:
                        print("Cannot change your own access level.")
                        # Handle the error as desired, e.g. by sending an email notification or logging the error
                        return None
                else:
                    raise  # Re-raise the exception if it's not related to the access level change

            print(f'Calendar created: {new_calendar.get("id")}')
    
    ###########################################################################
    
    ###########################################################################
    # Load a list of calendars

    def load_calendars(self):
        calendars_result = self.calendar_service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        return calendars
    
    ###########################################################################
    
    ###########################################################################
    # Load a list of events from a calendar

    def load_events(self, calendar_id):
        time_min = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        time_max = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
        events_result = self.calendar_service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get("items", [])

        return events
        # # Print the events
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(f'{start} {event["summary"]}')
    
    ###########################################################################
    
    ###########################################################################
    # Update an event on a calendar
    # UNUSED IN DEMO

    def update_event(self, calendar_id, event_id, updates):
        headers = {
            "Authorization": "Bearer {}".format(self.access_token),
            "Content-Type": "application/json"
        }
        url = "{}/calendars/{}/events/{}".format(self.calendar_api_base_url, calendar_id, event_id)
        response = requests.patch(url, headers=headers, data=json.dumps(updates))
        return response.json()
    
    ###########################################################################
    
    ###########################################################################
    # Update an event on a calendar
    # UNUSED IN DEMO
    
    def invite_to_calendar(self, calendar_id, email, role):
        calendar = self.service.calendars().get(calendarId=calendar_id).execute()
        calendar['guestsCanSeeGuests'] = True
        self.service.calendars().patch(calendarId=calendar_id, body=calendar).execute()
        self.service.acl().insert(calendarId=calendar_id, body={
            'scope': {'type': 'user', 'value': email},
            'role': role
        }).execute()

    ###########################################################################

#  End of Google Calendar API
###############################################################################