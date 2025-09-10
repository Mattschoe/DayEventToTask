import datetime
import os.path

import datetime
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#PATHS
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

CALENDAR_TOKEN_PATH = os.path.join(DATA_DIR, "calendarToken.json")
TASKS_TOKEN_PATH = os.path.join(DATA_DIR, "tasksToken.json")
CALENDAR_ID_PATH = os.path.join(DATA_DIR, "calendarID.data")


#SCOPES
CALENDER_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TASKS_SCOPES = ["https://www.googleapis.com/auth/tasks"]

def main():
    calendarCreds = getCalendarCredentials()
    tasksCreds = getTasksCredentials()
    calendarID = getCalenderID()
    events = loadTodayDailyEvents(calendarCreds, calendarID)
    insertIntoTasks(events, tasksCreds)

#Tries to load today's daily events
def loadTodayDailyEvents(credentials, calendarID):
    if not calendarID:
        print("No calendarID provided. Exiting.")
        return

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
            ).execute()
        )
        events = eventsResult.get("items", [])

        if not events:
            print("No tasks for today! Enjoy your day :)")
            return

        #Returns every "all_day" event
        return [event for event in events if "date" in event["start"]]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return

#Converts the daily events into tasks
def insertIntoTasks(eventsToday, credentials):
    try:
        service = build("tasks", "v1", credentials=credentials)
        #Creates a new list for the day
        todaysList = service.tasklists().insert(body = {
            "title": datetime.datetime.today().strftime("%d-%m-%Y")
        }).execute()

        for event in eventsToday:
            service.tasks().insert(tasklist=todaysList.get("id"), body = {
                "title": event["summary"],
            }).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")

#Writes base64 enviroment variables to file
def writeB64EnvToFile(envName, path):
    val = os.getenv(envName)
    if val:
        try:
            with open(path, "wb") as file:
                file.write(base64.b64decode(val))
        except Exception as e:
            print("Failed to write", path, "from env", envName, e)

#Reads the API-access and returns the credentials
def getCalendarCredentials():
    #If secret was set in GitHub, write to file so rest of code can use it
    writeB64EnvToFile("CALENDAR_TOKEN_B64", CALENDAR_TOKEN_PATH)

    credentials = None

    #Tries to load existing credentials from file
    if os.path.exists(CALENDAR_TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(CALENDAR_TOKEN_PATH, CALENDER_SCOPES)

    #If not, we let the user log in first
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            #If user is not logged in, but it's CI/Actions running the program exit, user needs to log in first
            if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true":
                raise RuntimeError("No valid calendar token found. In CI, set CALENDAR_TOKEN_B64 (base64 of calendarToken.json), before letting CI run program.")

            #Manual login from user (Should be one-time only)
            print("No credentials file found for creating token, please provide the path for credentials.json:")
            credPath = askUserForCredentials()
            flow = InstalledAppFlow.from_client_secrets_file(credPath, CALENDER_SCOPES)
            credentials = flow.run_local_server(port=0)
            print("Saving credentials as calendarToken.json for next time...")
            with open(CALENDAR_TOKEN_PATH, "w") as token:
                token.write(credentials.to_json())

    return credentials

#Reads the API-access and returns the credentials
def getTasksCredentials():
    # If secret was set in GitHub, write to file so rest of code can use it
    writeB64EnvToFile("TASKS_TOKEN_B64", TASKS_TOKEN_PATH)

    credentials = None

    #If the user has already created a token
    if os.path.exists(TASKS_TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TASKS_TOKEN_PATH, TASKS_SCOPES)

    #If not, we let the user log in first
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            #If user is not logged in, but it's CI/Actions running the program exit, user needs to log in first
            if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true":
                raise RuntimeError(
                    "No valid calendar token found. In CI, set TASKS_TOKEN_64 (base64 of tasksToken.json), before letting CI run program.")

            #Manual login from user (Should be one-time only)
            print("No credentials file found for creating token, please provide the path for credentials.json:")
            credPath = askUserForCredentials()
            flow = InstalledAppFlow.from_client_secrets_file(credPath, TASKS_SCOPES)
            credentials = flow.run_local_server(port=0)
            print("Saving credentials as token.json for next time...")
            with open(TASKS_TOKEN_PATH, 'w') as token:
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
    #If Actions/CI we just return the enviroment variable
    envCalID = os.environ.get("CALENDAR_ID")
    if envCalID:
        return envCalID

    #Else we fallback to the stored file
    if os.path.exists(CALENDAR_ID_PATH):
        with open(CALENDAR_ID_PATH, 'r') as file:
            file.readline().strip()
    else:
        #Saves CalendarID (should be one-time only)
        print("Please provide CalendarID for the calendar that stores the daily events:")
        calenderID = input().strip()
        with open(CALENDAR_ID_PATH, 'w') as file:
            file.write(calenderID)
        return calenderID

if __name__ == "__main__":
    main()