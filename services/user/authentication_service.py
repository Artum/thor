from logging import getLogger


log = getLogger(__name__)

class AuthenticationService:

    def validate_google_oauth_token(oauth_token: str, subject: str, client_id: str):
        """
        https://developers.google.com/identity/sign-in/web/backend-auth#python
        """
        from google.oauth2 import id_token
        from google.auth.transport import requests

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(id_token=oauth_token, request=requests.Request(), audience=client_id)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            subject_from_token = idinfo['sub']
            if subject_from_token != subject:
                raise ValueError("Mismatch in subject")

        except ValueError as e:
            # Invalid token
            log.error(f"Failed to validate token: {e}")
            raise
