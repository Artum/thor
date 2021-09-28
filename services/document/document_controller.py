from .document_service import DocumentService
from models.document import Document
from typing import Iterable, Optional


class DocumentController:

    @staticmethod
    def get_all_documents(user_id: str, field: Optional[str], sort: Optional[str]) -> Iterable[Document]:
        return DocumentService.get_all_documents(user_id=user_id, field=field, sort=sort)

    @staticmethod
    def get_document_by_id(user_id:str, id: str) -> Optional[Document]:
        return DocumentService.get_document_by_id(user_id=user_id, id=id)

    @staticmethod
    def delete_document(user_id:str, id: str):
        return DocumentService.delete_document(user_id=user_id, id=id)


    @staticmethod
    def get_document_content_by_id(user_id:str, id: str) -> Optional[bytes]:
        document = DocumentService.get_document_by_id(user_id=user_id, id=id)
        if not document:
            return None
        return DocumentService.get_document_content(document_path=document.document_path)

    @staticmethod
    def handle_document_upload(user_id: str, file_name: str, file_content) -> str:
        new_file, hash, storage_path = DocumentService.store_document_file(user_id=user_id, file_content=file_content)
        if new_file:
            DocumentService.create_document(user_id, file_name, hash, storage_path)
        return hash