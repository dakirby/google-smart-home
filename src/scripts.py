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
    smc.get_cfg()

    # Generate workout using generative AI
    # Store workout as event in user's Google Calendar


def debug(args):
    from device_modules.identity_manager import IdentityManager
    from pathlib import Path
    from device_modules.secret_manager_caller import SecretManagerCaller

    credential_json_path = Path(__file__).parent / "credentials.json"
    user_id = IdentityManager.google_oauth2_login(
        credential_json_path=credential_json_path
    )

    smc = SecretManagerCaller(user_id=user_id)

    # smc.create_secret("cfg")

    # smc.add_secret_version("cfg", {"version": "0.0.1"})

    smc.get_cfg()

    pass
