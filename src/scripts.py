def start_up(args: dict):
    """Flow for starting the app.

    Args:
        args (dict): a dictionary of key word arguments to alter the start up.
    """
    # Authenticate user
    from device_modules.identity_manager import IdentityManager
    from pathlib import Path

    credential_json_path = Path(__file__).parent / "credentials.json"
    user_id = IdentityManager.google_oauth2_login(
        credential_json_path=credential_json_path
    )

    # Get user configuration data
    from device_modules.secret_manager_caller import SecretManagerCaller

    smc = SecretManagerCaller(user_id=user_id)
    usercfg = smc.get_cfg()

    # Check if workout event scheduled for today
    from device_modules.googlecalendar_manager import GcalendarManager

    gcm = GcalendarManager(user_id=user_id, usercfg=usercfg)
    workout_scheduled_bool = gcm.check_for_workout()

    # Generate workout using generative AI; store in calendar
    if not workout_scheduled_bool:
        from device_modules.googleai_caller import GoogleAICaller

        gai_caller = GoogleAICaller(user_id=user_id, usercfg=usercfg)
        workout_text = gai_caller.get_new_workout()
        gcm.create_workout_event(workout_text)


def debug(args):
    start_up(args)

    pass
