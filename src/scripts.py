from pathlib import Path


def debug(args):
    from device_modules.identity_manager import IdentityManager

    credential_json_path = Path(
        r"D:\paper_repos\google-smart-home\google-smart-home\src\credentials.json"
    )
    identity_manager = IdentityManager.google_oauth2_login(
        credential_json_path=credential_json_path
    )
    pass
