import datetime

from services.authentication_service import AuthenticationService
from services.user_service import UserService
from services.access_token_service import AccessTokenService
from config import Config


class UserController:

    @staticmethod
    def authenticate_access(id_token: str, user_id: str, user_full_name: str, user_first_name: str, user_last_name: str, user_email: str) -> str:
        # Validate parameters
        if not id_token or not user_id or not user_full_name or not user_first_name or not user_email:
            raise ValueError(f"Missing mandatory parameters")

        # Currently supported only the Google OAuth 2.0 
        AuthenticationService.validate_google_oauth_token(oauth_token=id_token, subject=user_id, client_id=Config.GOOGLE_CLIENT_ID)

        user = UserService.get_user_by_id(user_id)
        if not user:
            access_token = AccessTokenService.create_access_token(identity=user_id, expires_delta=datetime.timedelta(hours=8))
            user = UserService.create_user(
                user_id=user_id,
                access_token=access_token,
                user_full_name=user_full_name,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                user_email=user_email
            )
        else:
            is_expired = AccessTokenService.is_access_token_expired(access_token=UserService.get_user_access_token(user))
            if is_expired:
                access_token = AccessTokenService.create_access_token(identity=user_id, expires_delta=datetime.timedelta(hours=8))
                UserService.update_access_token(user=user, access_token=access_token)
        
        return UserService.get_user_access_token(user)
            