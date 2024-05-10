from google.cloud import secretmanager
from pathlib import Path
from device_modules.identity_manager import IdentityManager


class SecretManagerCaller:
    def __init__(self, user_id: IdentityManager):
        self.user_id = user_id
        self.PROJECT_ID = self.user_id.PROJECT_ID
        self.client = secretmanager.SecretManagerServiceClient(credentials=self.user_id)

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
            secret_id=secret_id, parent=parent, secret=secret
        )

        # Print the new secret name.
        print(f"Created secret: {response.name}")

    def add_secret_version(self, secret_id: str, secret_value: str):
        """Adds a value for a secret on Google Secret Manager. The secret value is appended as a version for the secret corresponding to secret_id.
        #TODO: link version to user's Google OAuth 2.0 credentials
        #TODO: test this before using
        Args:
            secret_id (str): _description_
            secret_value (str): _description_
        """

        # Build the resource name of the parent secret.
        parent = f"projects/{self.PROJECT_ID}/secrets/{secret_id}"

        # Convert the string secret_value into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the secret_value argument.
        secret_value = secret_value.encode("UTF-8")

        # Add the secret version.
        response = self.client.add_secret_version(
            parent=parent, secret_value={"data": secret_value}
        )

        # Print the new secret version name.
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id: str, version_id: str = "latest"):
        """Accesses the API key or other credential stored in the secret on Google Secret Manager.
        #TODO: test this before using
        Args:
            secret_id (str): The secret's id
            version_id (str, optional): Identifies which value of the secret to access. Defaults to "latest". #TODO: link to user's OAuth 2.0 credentials
        """

        # Build the resource name of the secret version.
        name = f"projects/{self.PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = self.client.access_secret_version(name=name)

        # Return the decoded payload.
        return response.payload.data.decode("UTF-8")
