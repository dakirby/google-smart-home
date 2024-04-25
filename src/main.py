import argparse
from scripts import debug


def main(args):
    from device_modules.identity_manager import IdentityManager
    from pathlib import Path

    credential_json_path = Path(__file__).parent / "credentials.json"
    user_identity = IdentityManager.google_oauth2_login(
        credential_json_path=credential_json_path
    )

    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_debug = subparsers.add_parser("debug")
    parser_debug.set_defaults(func=debug)

    parser.set_defaults(func=main)

    args = parser.parse_args()

    args.func(args)
