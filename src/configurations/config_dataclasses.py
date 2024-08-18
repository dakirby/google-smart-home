from __future__ import annotations

import dataclasses
from dataclasses import dataclass
import json


def cleanup(path):
    """Removes JSON files with API keys.
    For now, function does nothing. In production, should delete the JSON file.

    Args:
        path (Path): Path to the API key
    """
    pass


@dataclass
class UserCfg:
    open_weather_cfg: OpenWeatherCfg
    google_calendar_cfg: GoogleCalendarCfg
    google_ai_cfg: GoogleAICfg
    version: str

    @classmethod
    def from_dict(cls, dict_obj: dict) -> UserCfg:
        open_weather_cfg = OpenWeatherCfg(**dict_obj["open_weather_cfg"])
        google_calendar_cfg = GoogleCalendarCfg(**dict_obj["google_calendar_cfg"])
        google_ai_cfg = GoogleAICfg(**dict_obj["google_ai_cfg"])
        return cls(
            open_weather_cfg=open_weather_cfg,
            google_calendar_cfg=google_calendar_cfg,
            google_ai_cfg=google_ai_cfg,
            version=dict_obj["version"],
        )

    @staticmethod
    def _get_field_update_method(dataclass_name: str, args):
        if dataclass_name == "OpenWeatherCfg":
            return OpenWeatherCfg.update_param_dict(args)
        elif dataclass_name == "GoogleCalendarCfg":
            return GoogleCalendarCfg.update_param_dict(args)
        elif dataclass_name == "GoogleAICfg":
            return GoogleAICfg.update_param_dict(args)

    @classmethod
    def list_cfg_parameters(cls) -> list:
        """Provides a list of all fields of the UserCfg class plus all the fields of each UserCfg field which is a dataclass.
        Assumes all fields of UserCfg are either dataclasses or strings.

        Returns:
            list: all fields of UserCfg and all fields of each dataclass within UserCfg
        """
        attributes_list = [field.name for field in dataclasses.fields(UserCfg)]
        parameters_list = []
        for a in attributes_list:
            if type(a) is not str:
                for field in dataclasses.fields(a):
                    parameters_list.append(field)
        return attributes_list + parameters_list

    @classmethod
    def update_cfg_dict(cls, old_cfg_dict: dict) -> dict:
        """Updates a configuration dict with new values as needed, keeping old values from old_cfg_dict.

        Args:
            old_cfg_dict (dict): A dictionary of old configuration values.

        Returns:
            dict: A new configuration dictionary.
        """
        new_cfg_dict = {}
        # Update non-dataclass fields first
        from _version import __version__

        new_cfg_dict.update({"version": __version__})
        # Update dataclass fields
        for f in dataclasses.fields(UserCfg):
            if f.type != "str":
                new_param_dict = cls._get_field_update_method(f.type, old_cfg_dict)
                new_cfg_dict.update({f.name: new_param_dict[f.name]})
        return new_cfg_dict


@dataclass
class OpenWeatherCfg:
    lat: float
    long: float
    api_key: str

    def update_param_dict(old_dict: dict) -> dict:
        """Generates a new dict with updated parameter values if any were missing from old_dict.

        Args:
            old_dict (dict): A dictionary of parameter values which may or may not contain values for the parameters needed to create an instance of this class.

        Returns:
            dict: An updated dict obj with missing parameter values now included.
        """
        api_path = "src/openweather_id.json"
        param_dict_name = "open_weather_cfg"

        if param_dict_name not in old_dict.keys():
            old_dict.update({param_dict_name: {}})
        # User defined inputs:
        if "lat" not in old_dict[param_dict_name].keys():
            lat = input("Enter your latitude: ")
            old_dict[param_dict_name].update({"lat": lat})
        if "long" not in old_dict[param_dict_name].keys():
            long = input("Enter your longitude: ")
            old_dict[param_dict_name].update({"long": long})
        # JSON files
        if "api_key" not in old_dict[param_dict_name].keys():
            with open(api_path) as f:
                api_dict = json.load(f)
                old_dict[param_dict_name].update(
                    {"api_key": api_dict["OPENWEATHER_ID"]}
                )
        cleanup(api_path)
        return old_dict


@dataclass
class GoogleCalendarCfg:
    calender_id: str

    def update_param_dict(old_dict: dict) -> dict:
        """Generates a new dict with updated parameter values if any were missing from old_dict.

        Args:
            old_dict (dict): A dictionary of parameter values which may or may not contain values for the parameters needed to create an instance of this class.

        Returns:
            dict: An updated dict obj with missing parameter values now included.
        """
        api_path = "src/calendar_id.json"
        param_dict_name = "google_calendar_cfg"

        if param_dict_name not in old_dict.keys():
            old_dict.update({param_dict_name: {}})
        # User defined inputs:
        #   None

        # JSON files
        if "calender_id" not in old_dict[param_dict_name].keys():
            with open(api_path) as f:
                api_dict = json.load(f)
                old_dict[param_dict_name].update(
                    {"calender_id": api_dict["CALENDAR_ID"]}
                )
        cleanup(api_path)
        return old_dict


@dataclass
class GoogleAICfg:
    google_ai_id: str

    def update_param_dict(old_dict: dict) -> dict:
        """Generates a new dict with updated parameter values if any were missing from old_dict.

        Args:
            old_dict (dict): A dictionary of parameter values which may or may not contain values for the parameters needed to create an instance of this class.

        Returns:
            dict: An updated dict obj with missing parameter values now included.
        """
        api_path = "src/google_ai_id.json"
        param_dict_name = "google_ai_cfg"

        if param_dict_name not in old_dict.keys():
            old_dict.update({param_dict_name: {}})
        # User defined inputs:
        #   None

        # JSON files
        if "google_ai_id" not in old_dict[param_dict_name].keys():
            with open(api_path) as f:
                api_dict = json.load(f)
                old_dict[param_dict_name].update(
                    {"google_ai_id": api_dict["GOOGLE_AI_ID"]}
                )
        cleanup(api_path)
        return old_dict


@dataclass
class SenseMonitorCfg:
    """Unused for now"""

    token: str


if __name__ == "__main__":
    dict_obj = {
        "open_weather_cfg": {"lat": 54.533, "long": 54.423, "api_key": "key"},
        "google_calendar_cfg": {"calender_id": "some_id"},
        "google_ai_cfg": {"google_ai_id": "some_id"},
        "version": "0.0.1",
    }
    user_cfg = UserCfg.from_dict(dict_obj=dict_obj)

    print(user_cfg)
    pass
