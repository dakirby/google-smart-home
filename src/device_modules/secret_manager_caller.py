import json
from google.cloud import secretmanager
from pathlib import Path


class SecretManagerCaller:
    def __init__(self):
        self.PROJECT_ID = self._fetch_project_id()

    def _fetch_project_id(self):
        cloudproject_path = Path(__file__).parent.parent / "cloudproject.json"
        with open(cloudproject_path, "r") as f:
            data = json.load(f)
        return data["PROJECT_ID"]

    def create_secret(self, secret_id: str):
        """Creates a secret hosted on Google Secret Manager, which has a descriptive secret_id.

        Args:
            secret_id (str): the name used to identify the secret, such as API_key_for_XXX
        """
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the parent project.
        parent = f"projects/{self.PROJECT_ID}"

        # Build a dict of settings for the secret
        secret = {"replication": {"automatic": {}}}

        # Create the secret
        response = client.create_secret(
            secret_id=secret_id, parent=parent, secret=secret
        )

        # Print the new secret name.
        print(f"Created secret: {response.name}")

    def add_secret_version(self, secret_id: str, secret_value: str):
        """Adds a value for a secret on Google Secret Manager. The secret value is appended as a version for the secret corresponding to secret_id.
        #TODO: link version to user's Google OAuth 2.0 credentials
        Args:
            secret_id (str): _description_
            secret_value (str): _description_
        """
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the parent secret.
        parent = f"projects/{self.PROJECT_ID}/secrets/{secret_id}"

        # Convert the string secret_value into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the secret_value argument.
        secret_value = secret_value.encode("UTF-8")

        # Add the secret version.
        response = client.add_secret_version(
            parent=parent, secret_value={"data": secret_value}
        )

        # Print the new secret version name.
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id: str, version_id: str = "latest"):
        """Accesses the API key or other credential stored in the secret on Google Secret Manager.

        Args:
            secret_id (str): The secret's id
            version_id (str, optional): Identifies which value of the secret to access. Defaults to "latest". #TODO: link to user's OAuth 2.0 credentials
        """
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{self.PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(name=name)

        # Return the decoded payload.
        return response.payload.data.decode("UTF-8")


def main():
    test = SecretManagerCaller()
    print(test.PROJECT_ID)


if __name__ == "__main__":
    main()
