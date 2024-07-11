## Creating a new project

1. Download the project source code [here](https://github.com/dakirby/google-smart-home). Install all Python requirements outlined in `requirements.txt`
2. [Enable the Google Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager). Follow steps 1-3 in the linked page. Note that when enabling billing, you can set a billing limit on your project to just a few cents. This is just for extra safety; the project should not cost you anything since a sufficient number of API requests are allowed free of charge.
3. Set up application default credentials by [creating an OAuth 2.0 client ID](https://support.google.com/cloud/answer/6158849?hl=en). Select desktop app when asked for Application Type. Once the credentials are created, a pop-up screen will provide an opportunity to download the credentials JSON file. Save this file as `credentials.json` in the project `src` folder.
4. Find your Google Calendar ID.
    1. Open Google Calendar in your browser while logged into your Google account.

    2. Navigate to your `My calendars` list (usually bottom left side).

    3. If you want to use a new calendar for this project, create a new calendar now.

    4. To get to your calendar settings, hover over the calendar you wish to use for this project and click the three vertical dots that appear to the right – this will bring up a dropdown menu, click `Settings and sharing`. 

    5. A new page will open. Find the Calendar ID at the bottom under the Integrate Calendar section. The ID should be in the form `XXX@group.calendar.google.com`

    6. Create a file called `calendar_id.json` in the project `src` folder and save the Calendar ID in the file as: `{"CALENDAR_ID": XXX@group.calendar.google.com"}`