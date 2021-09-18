from flask import Blueprint, jsonify, abort, request
from logging import getLogger
from auth import jwt

from services.user import UserController

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
