import json
import os
import time
from flask import Blueprint, jsonify, abort, request
from oauth2client import client
from logging import getLogger
from sqlalchemy import inspect

from config import Config
from models.user import User

from database import db

__all__ = ["users_blueprint"]

log = getLogger(__name__)

users_blueprint = Blueprint(
    'users_blueprint',
    __name__
)

@users_blueprint.route('/user/<user_id>', methods=["GET"])
def get_user(user_id):
    log.debug(f"Get user with id: {user_id}")

    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404, description="User not found")
    result = user.to_dict()

    log.debug(f"Found user: {result}")
    return jsonify(result)

@users_blueprint.route('/create', methods=["POST"])
def create_user():
    user = request.json
    log.debug(f"Create user: {user}")

    new_user = User(**user)

    db.session.add(new_user)
    db.session.commit()

    result = new_user.to_dict()

    log.debug(f"New user: {result}")
    return jsonify(result)

@users_blueprint.route('/authorize', methods=["POST"])
def authorize():
    """
    https://developers.google.com/identity/sign-in/web/server-side-flow#python
    """
    
    auth_code = request.get_json()["auth_code"]
    log.debug(f"******** /api/authorize: auth_code = {auth_code}")
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

    log.debug(f"credentials = {credentials}")

    resp = jsonify(success=True)
    resp.status_code = 200
    return resp
