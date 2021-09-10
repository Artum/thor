from flask import Blueprint, jsonify, abort, request
from logging import getLogger
from auth import jwt

from services.user_controller import UserController

__all__ = ["user_blueprint"]

log = getLogger(__name__)

user_blueprint = Blueprint(
    'user_blueprint',
    __name__
)

@user_blueprint.route('/login', methods=["POST"])
def login():
    login_params = request.get_json()
    log.debug(f"login_params = {login_params}")
    
    # Auth parameters
    user_id = login_params.get("user_id")
    token = login_params.get("id_token")

    # User parameters
    user_full_name = login_params.get("full_name")
    user_first_name = login_params.get("first_name")
    user_last_name = login_params.get("last_name")
    user_email = login_params.get("email")


    access_token = UserController.authenticate_access(
        id_token=token, 
        user_id=user_id, 
        user_full_name=user_full_name, 
        user_first_name=user_first_name, 
        user_last_name=user_last_name,
        user_email=user_email
    )

    resp = jsonify({
        'user_id': user_id,
        'access_token': access_token
    })
    resp.status_code = 200
    return resp

# @user_blueprint.route('/authorize', methods=["POST"])
# @jwt_required
# def authorize():
#     """
#     https://developers.google.com/identity/sign-in/web/server-side-flow#python
#     """
    
#     auth_code = request.get_json()["auth_code"]
#     log.debug(f"auth_code = {auth_code}")
#     if not request.headers.get('X-Requested-With'):
#         abort(403)

#     # Exchange auth code for access token, refresh token, and ID token
#     credentials = client.credentials_from_code(
#         client_id=Config.GOOGLE_CLIENT_ID,
#         client_secret=Config.GOOGLE_CLIENT_SECRET,
#         scope=['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
#         code=auth_code
#     )
        
#     # TODO: Parse the credential object and store in DB needed info
#     """
#     access_token:'ya29.a0AfH6SMA0GFdO4a3ODqvqATTVQilJpQuFXktlP5ZUEFn8mgsE_kMCQ-20zr0G-Sx35E68XH9mQKy-PP55R42vX4kjA0HQrJ6Mxak1Hk9WOUyjfMgebpavarSrmN2EmFFzLXYWeOJz_E4JswfU5nubEQMeR9ig3gno26w'
#     access_token_expired:False
#     client_id:'526253080549-64b3tedvs9oqtgfseto9atnb2i5a6bcc.apps.googleusercontent.com'
#     client_secret:'9TSahsWi_sAjZVCctlYYnPqv'
#     id_token:{'at_hash': '-MpneMzTs_1x7po26X08Qw', 'aud': '526253080549-64b3ted...ontent.com', 'azp': '526253080549-64b3ted...ontent.com', 'email': 'aptem.tchachkin@gmail.com', 'email_verified': True, 'exp': 1602335973, 'family_name': 'Tchachkin', 'given_name': 'Artum', 'iat': 1602332373, 'iss': 'https://accounts.google.com', 'locale': 'en', 'name': 'Artum Tchachkin', 'picture': 'https://lh3.googleus...HB5w=s96-c', 'sub': '109812372639340839487'}
#     id_token_jwt:'eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkYTc4NjNlODYzN2Q2NjliYzJhMTI2MjJjZWRlMmE4ODEzZDExYjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MjYyNTMwODA1NDktNjRiM3RlZHZzOW9xdGdmc2V0bzlhdG5iMmk1YTZiY2MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MjYyNTMwODA1NDktNjRiM3RlZHZzOW9xdGdmc2V0bzlhdG5iMmk1YTZiY2MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDk4MTIzNzI2MzkzNDA4Mzk0ODciLCJlbWFpbCI6ImFwdGVtLnRjaGFjaGtpbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ii1NcG5lTXpUc18xeDdwbzI2WDA4UXciLCJuYW1lIjoiQXJ0dW0gVGNoYWNoa2luIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpRFhfNkpUb1ZwTHgxOGUzc0k3S3NPOUpTaE1TVmFVdlhFMmFIQjV3PXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkFydHVtIiwiZmFtaWx5X25hbWUiOiJUY2hhY2hraW4iLCJsb2NhbGUiOiJlbiIsImlhdCI6MTYwMjMzMjM3MywiZXhwIjoxNjAyMzM1OTczfQ.QG79Jy6gYBpKSkc3kvdXDjRQFHBUUKm77QlYkQ3Uo_0aGuGy2rfqxBoY10IKFK9t-rvwbl3BzcHzVVJ1ymVdbaDPvKtMvHmoXco6TcGwi5-Yn5Ff249GN398l-P_J5TxCEHKqZ2znChu8GRKTgF0trSHv6995iPN7aNNePkXKJJVPRJR8NKMsSdtgdq8Z8pNQ...
#     invalid:False
#     refresh_token:'1//03O6ulfmUWZotCgYIARAAGAMSNwF-L9IrVcEgICpKgT9L8Xg4ZPdtXV3815r3RVwm0I8Rp2i23ce5Chtmm_-yuisaPP3ECLxES7g'
#     revoke_uri:'https://oauth2.googleapis.com/revoke'
#     scopes:{'email', 'https://www.googleapis.com/auth/drive.appdata', 'profile'}
#     store:None
#     token_expiry:datetime.datetime(2020, 10, 10, 13, 19, 25, 973576)
#     token_info_uri:'https://oauth2.googleapis.com/tokeninfo'
#     token_response:{'access_token': 'ya29.a0AfH6SMA0GFdO4...9ig3gno26w', 'expires_in': 3592, 'id_token': 'eyJhbGciOiJSUzI1NiIs...321G-Xou7Q', 'refresh_token': '1//03O6ulfmUWZotCgYI...P3ECLxES7g', 'scope': 'openid https://www.g...info.email', 'token_type': 'Bearer'}
#     token_uri:'https://oauth2.googleapis.com/token'
#     user_agent:None
#     """


#     log.debug(f"credentials = {credentials}")

#     resp = jsonify(success=True)
#     resp.status_code = 200
#     return resp



# @jwt.user_loader_callback_loader
# def jwt_load_user(user_id):
#     try:
#         token = request.headers.environ["HTTP_AUTHORIZATION"].split()[1]
#         user = UserController.get_user_with_token(user_id=user_id, access_token=token)
#         if not user:
#             abort(401, "Token mismatch")
#         return user
#     except Exception as ex:
#         log.exception(f"Failed to load user: {ex}")
#         abort(500, "Failed to load user")
