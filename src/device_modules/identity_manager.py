from __future__ import annotations
from pathlib import Path
from typing import Optional
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError


class IdentityManager:
    def __init__(self, creds: Credentials):
        """Contains identification details needed to verify a user.
         Use google_oauth2_login method to handle object creation.

        Args:
            creds (Credentials): google.oauth2.Credentials using OAuth 2.0 access and refresh tokens.
        """
        self.creds = creds
        self.secrets = self._fetch_secrets()
        self.PROJECT_ID = self._fetch_project_id()

    @classmethod
    def google_oauth2_login(
        cls,
        credential_json_path: Path | str,
        token_json_path: Optional[Path | str] = None,
    ) -> IdentityManager:
        """Creates an IdentityManager object which contains the google.oauth2.Credentials and
        necessary secrets for the project. Assumes token_json_path sits in the same directory as credential_json_path if token_json_path is not provided.

        Args:
            credential_json_path (Path | str): Path to the credentials.json file associated with the OAuth 2.0 enabled Google project.
            token_json_path (Optional[Path  |  str], optional): Path to the token.json file containing the credentials needed for OAuth 2.0 access. Defaults to None.

        Raises:
            ValueError: Provided credential_json_path does not exist.

        Returns:
            IdentityManager:  IdentityManager object which contains the google.oauth2.Credentials and necessary secrets for the project
        """
        if isinstance(credential_json_path, str):
            credential_json_path = Path(credential_json_path)
        if not credential_json_path.exists():
            # TODO: add custom errors
            raise ValueError(f"{credential_json_path=} doesn't exist")

        if token_json_path is None:
            creds = IdentityManager._fetch_google_credentials(
                credential_json_path=credential_json_path
            )

        return cls(creds=creds)

    @staticmethod
    def _fetch_google_credentials(
        credential_json_path: Path,
    ) -> Credentials:
        token_json_path = credential_json_path.parent / "token.json"
        creds = None
        if (token_json_path).exists():
            creds = Credentials.from_authorized_user_file(token_json_path)

        if not creds or (creds and not creds.valid):
            creds = IdentityManager._login_flow(credential_json_path, token_json_path)

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = IdentityManager._login_flow(
                    credential_json_path, token_json_path
                )

        return creds

    @staticmethod
    def _login_flow(credential_json_path: Path | str, token_json_path: Path | str):
        flow = InstalledAppFlow.from_client_secrets_file(
            credential_json_path,
            [
                "https://www.googleapis.com/auth/calendar.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ],
        )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json_path, "w") as f:
            f.write(creds.to_json())

        return creds

    def _fetch_secrets(self):
        # TODO: check creds and use creds to access secrets and acquire them
        secrets = {"openweather_api_key": "API_KEY"}
        return secrets

    def _fetch_project_id(self):
        # TODO: check credentials for project id
        cloudproject_path = Path(__file__).parent.parent / "cloudproject.json"
        with open(cloudproject_path, "r") as f:
            data = json.load(f)
        return data["PROJECT_ID"]
