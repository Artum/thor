import datetime

from flask_jwt_extended import create_access_token, decode_token
from jwt import ExpiredSignatureError

class AccessTokenService:

    @staticmethod
    def create_access_token(identity: str, expires_delta: datetime.timedelta) -> str:
        token = create_access_token(identity=identity, expires_delta=expires_delta)
        return token

    @staticmethod
    def is_access_token_expired(access_token: str) -> bool:
        try:
            decode_token(access_token)
            return False
        except ExpiredSignatureError:
            return True
