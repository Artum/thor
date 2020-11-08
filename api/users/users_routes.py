import json
import os
import time
import datetime

from flask import Blueprint, jsonify, abort, request
from flask_login import login_user
from flask_jwt_extended import jwt_required, create_access_token, decode_token, get_current_user
from jwt import ExpiredSignatureError
from oauth2client import client
from logging import getLogger
from sqlalchemy import inspect

from config import Config
from models.user import User

from database import db
from auth import jwt

__all__ = ["users_blueprint"]

log = getLogger(__name__)

users_blueprint = Blueprint(
    'users_blueprint',
    __name__
)

@users_blueprint.route('/login', methods=["POST"])
def login():
    login_params = request.get_json()
    log.debug(f"login_params = {login_params}")
    
    user_id = login_params["user_id"]
    token = login_params.pop("id_token", None)
    validate_token(token, user_id)

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        user = User(**login_params)
        user.token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(hours=8))
        db.session.add(user)
        db.session.commit()
    else:
        try:
            user_token = decode_token(user.token)
        except ExpiredSignatureError:
            user.token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(hours=8))
            db.session.add(user)
            db.session.commit()

    resp = jsonify({
        'user_id': user.user_id,
        'token': user.token
    })
    resp.status_code = 200
    return resp

@users_blueprint.route('/authorize', methods=["POST"])
@jwt_required
def authorize():
    """
    https://developers.google.com/identity/sign-in/web/server-side-flow#python
    """
    
    auth_code = request.get_json()["auth_code"]
    log.debug(f"auth_code = {auth_code}")
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = Config.GOOGLE_CLIENT_SECRET_FILE

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)
        
    # TODO: Parse the credential object and store in DB needed info
    """
    access_token:'ya29.a0AfH6SMA0GFdO4a3ODqvqATTVQilJpQuFXktlP5ZUEFn8mgsE_kMCQ-20zr0G-Sx35E68XH9mQKy-PP55R42vX4kjA0HQrJ6Mxak1Hk9WOUyjfMgebpavarSrmN2EmFFzLXYWeOJz_E4JswfU5nubEQMeR9ig3gno26w'
    access_token_expired:False
    client_id:'526253080549-64b3tedvs9oqtgfseto9atnb2i5a6bcc.apps.googleusercontent.com'
    client_secret:'9TSahsWi_sAjZVCctlYYnPqv'
    id_token:{'at_hash': '-MpneMzTs_1x7po26X08Qw', 'aud': '526253080549-64b3ted...ontent.com', 'azp': '526253080549-64b3ted...ontent.com', 'email': 'aptem.tchachkin@gmail.com', 'email_verified': True, 'exp': 1602335973, 'family_name': 'Tchachkin', 'given_name': 'Artum', 'iat': 1602332373, 'iss': 'https://accounts.google.com', 'locale': 'en', 'name': 'Artum Tchachkin', 'picture': 'https://lh3.googleus...HB5w=s96-c', 'sub': '109812372639340839487'}
    id_token_jwt:'eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkYTc4NjNlODYzN2Q2NjliYzJhMTI2MjJjZWRlMmE4ODEzZDExYjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MjYyNTMwODA1NDktNjRiM3RlZHZzOW9xdGdmc2V0bzlhdG5iMmk1YTZiY2MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MjYyNTMwODA1NDktNjRiM3RlZHZzOW9xdGdmc2V0bzlhdG5iMmk1YTZiY2MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDk4MTIzNzI2MzkzNDA4Mzk0ODciLCJlbWFpbCI6ImFwdGVtLnRjaGFjaGtpbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ii1NcG5lTXpUc18xeDdwbzI2WDA4UXciLCJuYW1lIjoiQXJ0dW0gVGNoYWNoa2luIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpRFhfNkpUb1ZwTHgxOGUzc0k3S3NPOUpTaE1TVmFVdlhFMmFIQjV3PXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkFydHVtIiwiZmFtaWx5X25hbWUiOiJUY2hhY2hraW4iLCJsb2NhbGUiOiJlbiIsImlhdCI6MTYwMjMzMjM3MywiZXhwIjoxNjAyMzM1OTczfQ.QG79Jy6gYBpKSkc3kvdXDjRQFHBUUKm77QlYkQ3Uo_0aGuGy2rfqxBoY10IKFK9t-rvwbl3BzcHzVVJ1ymVdbaDPvKtMvHmoXco6TcGwi5-Yn5Ff249GN398l-P_J5TxCEHKqZ2znChu8GRKTgF0trSHv6995iPN7aNNePkXKJJVPRJR8NKMsSdtgdq8Z8pNQ...
    invalid:False
    refresh_token:'1//03O6ulfmUWZotCgYIARAAGAMSNwF-L9IrVcEgICpKgT9L8Xg4ZPdtXV3815r3RVwm0I8Rp2i23ce5Chtmm_-yuisaPP3ECLxES7g'
    revoke_uri:'https://oauth2.googleapis.com/revoke'
    scopes:{'email', 'https://www.googleapis.com/auth/drive.appdata', 'profile'}
    store:None
    token_expiry:datetime.datetime(2020, 10, 10, 13, 19, 25, 973576)
    token_info_uri:'https://oauth2.googleapis.com/tokeninfo'
    token_response:{'access_token': 'ya29.a0AfH6SMA0GFdO4...9ig3gno26w', 'expires_in': 3592, 'id_token': 'eyJhbGciOiJSUzI1NiIs...321G-Xou7Q', 'refresh_token': '1//03O6ulfmUWZotCgYI...P3ECLxES7g', 'scope': 'openid https://www.g...info.email', 'token_type': 'Bearer'}
    token_uri:'https://oauth2.googleapis.com/token'
    user_agent:None
    """


    log.debug(f"credentials = {credentials}")

    resp = jsonify(success=True)
    resp.status_code = 200
    return resp




###################################################################################################
# Helper Functions
###################################################################################################
def validate_token(token: str, user_id: str):
    """
    https://developers.google.com/identity/sign-in/web/backend-auth#python
    """
    from google.oauth2 import id_token
    from google.auth.transport import requests

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), Config.GOOGLE_CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        user_id_from_token = idinfo['sub']
        if user_id_from_token != user_id:
            raise ValueError("Mismatch in user_id")

    except ValueError as e:
        # Invalid token
        log.error(f"Failed to validate token: {e}")
        raise


@jwt.user_loader_callback_loader
def jwt_load_user(user_id):
    try:
        token = request.headers.environ["HTTP_AUTHORIZATION"].split()[1]
        user = User.query.filter_by(user_id=user_id).first()
        if user.token != token:
            abort(401, "Token mismatch")
        return user
    except Exception as ex:
        log.exception(f"Failed to load user: {ex}")
        abort(500, "Failed to load user")
