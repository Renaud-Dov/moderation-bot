import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Calendar:
    def __init__(self, calendarID, tokenID, credentials):
        self.calendarID = calendarID
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(tokenID):
            with open(tokenID, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(tokenID, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def __GetEventsOfDay(self, day: datetime.datetime):
        now = day.isoformat() + 'Z'
        tomorrow = (day + datetime.timedelta(hours=12)).isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId=self.calendarID,
            timeMin=now, timeMax=tomorrow,
            maxResults=15, singleEvents=True,
            orderBy='startTime').execute()

        return events_result.get('items', [])

    def getClassOfTheDay(self):

        return self.__GetEventsOfDay(datetime.datetime.utcnow().replace(hour=7))

    def getClassOfTomorrow(self):
        return self.__GetEventsOfDay(datetime.datetime.utcnow().replace(hour=7) + datetime.timedelta(days=1))
