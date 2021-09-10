from services.document_controller import DocumentController

from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from logging import getLogger

from models.document import Document


__all__ = ["document_blueprint"]

log = getLogger(__name__)

document_blueprint = Blueprint(
    'document_blueprint',
    __name__
)

@document_blueprint.route('/', methods=["GET"])
@jwt_required
def get_all_documents():

    user_id = get_jwt_identity()
    documents = DocumentController.get_all_documents(user_id=user_id)
    resp = jsonify([x.to_dict() for x in documents])
    resp.status_code = 200
    return resp

@document_blueprint.route('/<id>', methods=["GET"])
#@jwt_required
def get_invoices(id: str):
    document = DocumentController.get_document_by_id(id)
    if not document:
        abort(404, "Document not found")

    resp = jsonify([x.to_dict() for x in Document.query.all()])
    resp.status_code = 200
    return resp

# @document_blueprint.route('/', methods=["POST"])
# @jwt_required
# def add_invoice():
#     params = request.get_json()
#     params.pop("id", None)
#     params["id"] = uuid.uuid4().hex
#     log.debug(f"params = {params}")
    
#     invoice = Document(**params)
#     db.session.add(invoice)
#     db.session.commit()
    
#     resp = jsonify(invoice.to_dict())
#     resp.status_code = 200
#     return resp


