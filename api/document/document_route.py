
from flask import Blueprint, jsonify, abort, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from logging import getLogger
from textwrap import wrap

from services.document import DocumentController


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
@jwt_required
def get_document(id: str):
    user_id = get_jwt_identity()
    document = DocumentController.get_document_by_id(user_id=user_id, id=id)
    if not document:
        abort(404, "Document not found")

    resp = jsonify(document.to_dict())
    resp.status_code = 200
    return resp

@document_blueprint.route('/<id>/content', methods=["GET"])
@jwt_required
def get_document_content(id: str):
    user_id = get_jwt_identity()
    content = DocumentController.get_document_content_by_id(user_id=user_id, id=id)
    if not content:
        abort(404, "Document not found")

    resp = jsonify(list(content))
    resp.status_code = 200
    return resp

@document_blueprint.route('/upload', methods=["POST"])
@jwt_required
def upload_document():
    user_id = get_jwt_identity()
    f = request.files['file']
    document_id = DocumentController.handle_document_upload(user_id=user_id, file_name=secure_filename(f.filename), file_content=f.read())
    resp = jsonify({
        "document_id": document_id
    })
    resp.status_code = 200
    return resp


