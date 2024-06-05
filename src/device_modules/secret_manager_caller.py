from google.cloud import secretmanager
from device_modules.identity_manager import IdentityManager
import json


class SecretManagerCaller:
    def __init__(self, user_id: IdentityManager):
        # Public attributes
        self.user_id = user_id
        self.PROJECT_ID = self.user_id.PROJECT_ID
        self.client = secretmanager.SecretManagerServiceClient(
            credentials=self.user_id.creds
        )

        # Private attributes
        self._CURRENT_CFG_VERSION = "0.0.2"

    def create_secret(self, secret_id: str):
        """Creates a secret hosted on Google Secret Manager, which has a descriptive secret_id.

        Args:
            secret_id (str): the name used to identify the secret, such as API_key_for_XXX
        """

        # Build the resource name of the parent project.
        parent = f"projects/{self.PROJECT_ID}"

        # Build a dict of settings for the secret
        secret = {"replication": {"automatic": {}}}

        # Create the secret
        response = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": secret,
            }
        )

        # Print the new secret name.
        print(f"Created secret: {response.name}")

    def add_secret_version(
        self, secret_id: str, payload: str
    ) -> secretmanager.SecretVersion:
        """Adds a value for a secret on Google Secret Manager. The secret value is appended as a version for the secret corresponding to secret_id.
        If the secret value is not a str object, the function will attempt to convert the payload to a json string.
        Args:
            secret_id (str): _description_
            secret_value (str): _description_
        """
        # Check if payload is type str or try to convert to json string otherwise.
        if not isinstance(payload, str):
            payload = json.dumps(payload)

        # Build the resource name of the parent secret.
        parent = self.client.secret_path(self.PROJECT_ID, secret_id)

        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        payload_bytes = payload.encode("UTF-8")

        # Add the secret version.
        response = self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {
                    "data": payload_bytes,
                },
            }
        )

        # Print the new secret version name.
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id: str, version_id: str = "latest"):
        """Accesses the API key or other credential stored in the secret on Google Secret Manager. Attempts to deserialize json string object before returning secret value.
        Args:
            secret_id (str): The secret's id
            version_id (str, optional): Identifies which value of the secret to access. Defaults to "latest". #TODO: link to user's OAuth 2.0 credentials
        """
        # Build the resource name of the secret version.
        name = f"projects/{self.PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = self.client.access_secret_version(name=name)

        # Decode payload and deserialize json string to python object.
        response_decoded = response.payload.data.decode("UTF-8")
        response_decoded = json.loads(response_decoded)
        return response_decoded

    def _cfg_exists(self):
        """Checks if configuration file exists as client secret. Config file must be saved with secret_id 'cfg' upon secret creation."""
        # Build list of all secrets viewable with current permissions
        parent = f"projects/{self.PROJECT_ID}"
        secrets_list = [
            secret.name.rsplit("/", 1)[-1]
            for secret in self.client.list_secrets(request={"parent": parent})
        ]

        # Check if cfg in secrets list
        if "cfg" in secrets_list:
            return True
        else:
            return False

    def _cfg_version_up_to_date(self):
        """Checks if current configuration file version is the latest configuration version.
        Assumes the configuration file already exists as a client secret."""

        current_cfg = self.access_secret_version("cfg")
        return current_cfg["version"] == self._CURRENT_CFG_VERSION

    def _create_or_update_cfg(self, create=False):
        """Updates missing records in configuration file.
        Uploads the new configuration file as client secret.

        Args:
            create (bool, optional): Set create=True if cfg does not exist so that new Google Secret Manager secret is created first. Defaults to False.

        Returns:
            bool: True if successful
        """
        # Create new secret if cfg does not already exist
        if create:
            self.create_secret("cfg")
            self.add_secret_version("cfg", {"version": self._CURRENT_CFG_VERSION})

        # Access current cfg
        cfg = self.access_secret_version("cfg")

        # Check for missing records and update information
        if "lat" not in cfg.keys():
            lat = input("Enter your latitude: ")
            cfg["lat"] = float(lat)

        # cfg version should now match _CURRENT_CFG_VERSION
        cfg["version"] = self._CURRENT_CFG_VERSION

        # Upload new record to Google Secret Manager
        self.add_secret_version("cfg", cfg)
        return True

    def get_cfg(self):
        """Gets the configuration file stored on Google Secret Manager.
        If the existing configuration file is not up to date, requests missing information from the user via the command line.

        Returns:
            Dict: configuration information stored as a dictionary.
        """
        if not self._cfg_exists():
            self.cfg = self._create_or_update_cfg(create=True)
        elif not self._cfg_version_up_to_date():
            self.cfg = self._create_or_update_cfg()
        else:
            self.cfg = self.access_secret_version("cfg")
        return self.cfg
