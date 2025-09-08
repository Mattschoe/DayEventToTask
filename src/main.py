import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def main():
    credentials = getCredentials()
    calenderID = getCalenderID()
    assert credentials is not None and calenderID is not None
    allDayEvents = loadTodayDailyEvents(credentials, calenderID)



#Tries to load today's daily events
def loadTodayDailyEvents(credentials, calendarID):
    calendarID = calendarID
    try:
        service = build("calendar", "v3", credentials=credentials)

        today = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat() + 'Z'

        #Calls calendar API
        eventsResult = (
            service.events()
            .list(
                calendarId = calendarID,
                timeMin = today,
                timeMax = tomorrow,
                maxResults = 100,
                singleEvents = True,
                orderBy = "startTime"
            )
            .execute()
        )
        events = eventsResult.get("items", [])

        if not events:
            print("No tasks for today! Enjoy your day :)")
            return

        #Returns every "all_day" event
        return [event for event in events if "date" in event["start"]]


    except HttpError as error:
        print(f"An error occurred: {error}")



#Reads the API-access and returns the credentials
def getCredentials():
    credentials = None

    #If the user has already created a token
    if os.path.exists('../data/token.json'):
        credentials = Credentials.from_authorized_user_file("../data/token.json", SCOPES)

    #If not, we let the user log in first
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            print("No credentials file found for creating token, please provide the path for credentials.json:")
            credPath = askUserForCredentials()
            flow = InstalledAppFlow.from_client_secrets_file(credPath, SCOPES)
            credentials = flow.run_local_server(port=0)
            print("Saving credentials as token.json for next time...")
            with open('../data/token.json', 'w') as token:
                token.write(credentials.to_json())

    return credentials

#Keeps asking user for a correct path to credentials
def askUserForCredentials():
    while True:
        credPath = input().replace("\"", "")
        if os.path.isfile(credPath):
            return credPath
        else:
            print("Path doesn't exist. Please try again.")
            continue

#Asks user if they want to just used the stored calender (if one is stored), otherwise ask user to provide one (which will be saved)
def getCalenderID():
    if os.path.exists('../data/calendarID.data'):
        file = open("../data/calendarID.data", 'r')
        calenderID = file.readline()
        file.close()
    else:
        print("Please provide CalendarID for the calendar that stores the daily events:")
        calenderID = input()

        #Saves CalendarID
        open("../data/calendarID.data", 'w').write(calenderID)

    return calenderID



if __name__ == "__main__":
    main()