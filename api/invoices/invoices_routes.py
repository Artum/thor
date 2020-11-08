import json
import os
import time
import datetime
import uuid

from flask import Blueprint, jsonify, abort, request
from flask_login import login_user
from flask_jwt_extended import jwt_required, create_access_token, decode_token, get_current_user
from jwt import ExpiredSignatureError
from oauth2client import client
from logging import getLogger
from sqlalchemy import inspect

from config import Config
from models.invoice import Invoice

from database import db
from auth import jwt

__all__ = ["invoices_blueprint"]

log = getLogger(__name__)

invoices_blueprint = Blueprint(
    'invoices_blueprint',
    __name__
)

@invoices_blueprint.route('/', methods=["GET"])
#@jwt_required
def get_invoices():
    resp = jsonify([x.to_dict() for x in Invoice.query.all()])
    resp.status_code = 200
    return resp

@invoices_blueprint.route('/', methods=["POST"])
#@jwt_required
def add_invoice():
    params = request.get_json()
    params.pop("id", None)
    params.pop("time_created", None)
    params.pop("time_updated", None)
    params["id"] = uuid.uuid4().hex
    log.debug(f"params = {params}")
    
    invoice = Invoice(**params)
    db.session.add(invoice)
    db.session.commit()
    
    resp = jsonify(invoice.to_dict())
    resp.status_code = 200
    return resp


