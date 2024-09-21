from configurations.config_dataclasses import UserCfg
from device_modules.identity_manager import IdentityManager


class GcalendarManager:
    def __init__(self, user_id: IdentityManager, usercfg: UserCfg):
        """Manages accessing and creating events in user's Google calendar as well as checking for scheduled workouts.

        Args:
            creds (Credentials): google.oauth2.Credentials using OAuth 2.0 access and refresh tokens.
        """
        self.user_id = user_id
        self.cfg = usercfg
        self.CALENDAR_ID = self.cfg.google_calendar_cfg.calender_id

    @staticmethod
    def _summarize_events(events_result):
        """Print descriptive event summaries.

        Args:
            events_result (Any): result of gcalendar_service.events().list().execute()
        """
        event_summaries = [e.get("summary") for e in events_result.get("items", [])]
        for es in event_summaries:
            print(es)

    def list_events(self, n_events, future=True):
        """List events in Google Calendar. Can be either past events or future events (defaults to future events).

        Args:
            n_events (_type_): The maximum number of events to retrieve.
            future (bool, optional): If True then lists upcoming events; if False then lists past events. Defaults to True.

        Returns:
            list: List of events
        """
        import datetime
        from googleapiclient.discovery import build

        # Instantiate Google Calendar API
        gcalendar_service = build("calendar", "v3", credentials=self.user_id.creds)
        now = (
            datetime.datetime.now(datetime.UTC).isoformat()
        )  # online documentation uses deprecated datetime method; code updated

        if future:
            events_result = (
                gcalendar_service.events()
                .list(
                    calendarId=self.CALENDAR_ID,
                    timeMin=now,
                    maxResults=n_events,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        else:
            events_result = (
                gcalendar_service.events()
                .list(
                    calendarId=self.CALENDAR_ID,
                    timeMax=now,
                    maxResults=n_events,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        return events_result

    def check_for_workout(self, end_check_time: int = 24) -> bool:
        """Checks to see if a workout is scheduled between now and `end_check_time`.

        Args:
            end_check_time (int, optional): number of hours into the future to check for a scheduled workout. Defaults to 24.

        Returns:
            bool: _description_
        """
        import datetime

        events_result = self.list_events(
            end_check_time * 2
        )  # Reasonable to guess that this is enough events to get.
        events = events_result.get("items", [])

        if not events:
            return False
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                time_diff = start - datetime.datetime.now()
                if time_diff.days * 24 + time_diff.seconds / 3600 >= end_check_time:
                    break
                else:
                    if "WORKOUT" in event.get("summary"):
                        return True
        return False  # If True has not been returned, no workouts scheduled

    def get_last_workout(self) -> str:
        """Finds the last workout in the calendar and returns a description of the event."""
        event_list = self.list_events(n_events=250, future=False)
        event_dict = event_list.get("items", [])[-1]
        return event_dict["description"]

    def create_workout_event(self, workout_info: str):
        from googleapiclient.discovery import build
        import datetime

        local_timezone = self.cfg.timezone_cfg.timezone  # Formatted as IANA timezone
        start_time = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()  # formatted according to RFC3339
        end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            seconds=3600
        )
        end_time = end_time.isoformat()  # formatted according to RFC3339

        new_workout_event = {
            "summary": "WORKOUT",
            "description": workout_info,
            "start": {
                "dateTime": start_time,
                "timeZone": local_timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": local_timezone,
            },
        }

        # Instantiate Google Calendar API
        gcalendar_service = build("calendar", "v3", credentials=self.user_id.creds)

        event = (
            gcalendar_service.events()
            .insert(
                calendarId=self.cfg.google_calendar_cfg.calender_id,
                body=new_workout_event,
            )
            .execute()
        )
        print(event)
