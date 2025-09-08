[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]

<!-- ABOUT THE PROJECT -->
## About The Project
As a vivid fan of planning my day and week with Google Calendar, i found a deep connection with marking a event "all-day" when it was just something i needed to get done at sometime during the day. The problem was that after my planning step, i would often try to "lock-in" and focus on the tasks at hand for the day. For this i often used googles "Tasks" which helps me track what i've done for the day and what i needed to do. But since some of my non-work tasks were in my calendar i would often distract myself by going back out of tasks and into calendar to make sure i didn't forget anything. This slowed my workflow and hindered me from every concentrating fully on something for the whole day. 

**No more!** \
With this tool, it will automatically convert the events marked with "all-day" in the calendar into a daily to-do list inside the Tasks. The project is meant to be used with GitHub Actions but modifications to code is allowed via the MIT license.

### Built With
This project uses Python to run the two libraries, both provided by Google Cloud.

API's used:
* [Google Tasks API](https://developers.google.com/workspace/tasks)
* [Google Calendar API](https://developers.google.com/workspace/calendar)

<!-- GETTING STARTED -->
## Quick Setup with GitHub Actions
This project is designed with GitHub Actions in mind. It can be locally run, but it won't make sense to do so because the program needs to be ran every day to create a new task.

### Prerequisites/Setup
#### Getting the credentials from Google Cloud
To use this project, credentials from Google Cloud are needed. This segment will focus on this process. \
**To Begin:**
1. Create a [Cloud project](https://developers.google.com/workspace/guides/create-project)
2. Enable the [Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com) and the [Tasks API](https://console.cloud.google.com/flows/enableapi?apiid=tasks.googleapis.com)
3. Enable [OAuth consent screen](https://developers.google.com/workspace/calendar/api/quickstart/python#configure_the_oauth_consent_screen)
4. Get the [``credentials.json``](https://developers.google.com/workspace/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application) file
5. Go to [Project Clients](https://console.cloud.google.com/auth/audience) and under _Test Users_ add the email you'll be using for the Google Calendar login later

#### Setting up tokens
This project needs a initial userlogin before it can be set up with Actions. This segment will focus on this process.
1. Fork the project
2. Clone to desktop
3. Move into the project and run the following commands:
```sh
  pip install -r requirements.txt
```
```sh
  cd src
```
```sh
  python main.py --setup
```
The project will require 2 inputs here. First: A path to the credentials.json file, this will also prompt a userlogin on the browser. Here choose the same email that you chose in _Project Clients_. Second: A calendarID. This ID is different for calendar to calendar and you can find it by going to the settings of your calendar and under **Integrate Calendar** you'll find _Calendar-ID_, it should end with _@group.calendar.google.com_. Paste this as the input for CalendarID in the CLI

Test the project works by running:
```sh
  python main.py --manual
```
Now you should see a Task list being created on [Tasks](https://tasks.google.com/). Otherwise please raise a [Issue](https://github.com/Mattschoe/DayEventToTask/issues)

### Setting up the GitHub Action
After running the setup there should be two new files in the local project, a ``CALENDER_ID.b64`` and a ``CREDENTIAL_TOKEN.b64`` file. If not, please repeat the Setup.
1. On Github go to the following: _Settings_ -> _Secrets And Variables_ -> _Actions_ -> _Repository Secrets_
2. Add a secret named _CALENDAR_ID_ and paste the context of ``CALENDER_ID.b64`` file as the secret value
3. Add a secret named _CREDENTIAL_TOKEN_ and paste the context of ``CREDENTIAL_TOKEN.b64`` file as the secret value

As a example for this project, the ``daily.yml`` workflow runs daily at 4am UTC time. This is personal preference and can just be changed.
Test the Action by going to: _Actions_ -> _Daily Calendar events to Tasks_ (example action) -> "run workflow". Now you should see a Task list being created on [Tasks](https://tasks.google.com/). Otherwise please raise a [Issue](https://github.com/Mattschoe/DayEventToTask/issues).

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Mattschoe/DayEventToTask.svg?style=for-the-badge
[contributors-url]: https://github.com/Mattschoe/DayEventToTask/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Mattschoe/DayEventToTask.svg?style=for-the-badge
[forks-url]: https://github.com/Mattschoe/DayEventToTask/forks
[stars-shield]: https://img.shields.io/github/stars/Mattschoe/DayEventToTask.svg?style=for-the-badge
[stars-url]: https://github.com/Mattschoe/DayEventToTask/stargazers
[issues-shield]: https://img.shields.io/github/issues/Mattschoe/DayEventToTask.svg?style=for-the-badge
[issues-url]: https://github.com/Mattschoe/DayEventToTask/issues
[license-shield]: https://img.shields.io/github/license/Mattschoe/DayEventToTask.svg?style=for-the-badge
[license-url]: https://github.com/Mattschoe/DayEventToTask/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
