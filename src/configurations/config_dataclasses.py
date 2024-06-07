from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserCfg:
    open_weather_cfg: OpenWeatherCfg
    google_calendar_cfg: GoogleCalendarCfg
    version: str

    @classmethod
    def from_dict(cls, dict_obj: dict) -> UserCfg:
        open_weather_cfg = OpenWeatherCfg(**dict_obj["open_weather_cfg"])
        google_calendar_cfg = GoogleCalendarCfg(**dict_obj["google_calendar_cfg"])
        return cls(
            open_weather_cfg=open_weather_cfg,
            google_calendar_cfg=google_calendar_cfg,
            version=dict_obj["version"],
        )


@dataclass
class OpenWeatherCfg:
    lat: float
    long: float
    api_key: str


@dataclass
class GoogleCalendarCfg:
    calender_id: str


@dataclass
class SenseMonitorCfg:
    """Unused for now"""

    token: str


if __name__ == "__main__":
    dict_obj = {
        "open_weather_cfg": {"lat": 54.533, "long": 54.423, "api_key": "key"},
        "google_calendar_cfg": {"calender_id": "some_id"},
        "version": "0.0.1",
    }
    user_cfg = UserCfg.from_dict(dict_obj=dict_obj)

    print(user_cfg)
    pass
