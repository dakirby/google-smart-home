from pathlib import Path


def debug(args):
    from device_modules.identity_manager import IdentityManager
    from pathlib import Path
    from device_modules.secret_manager_caller import SecretManagerCaller

    credential_json_path = Path(__file__).parent / "credentials.json"
    user_id = IdentityManager.google_oauth2_login(
        credential_json_path=credential_json_path
    )

    smc = SecretManagerCaller(user_id=user_id)
    # smc.create_secret("test_secret")

    pass
