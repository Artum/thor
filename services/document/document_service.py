from typing import Iterable, Optional, Tuple
import uuid
from models.document import Document
from database import db

class DocumentService:

   
    @staticmethod
    def get_all_documents(user_id: str) -> Iterable[Document]:
        documents = Document.query.filter_by(user_id=user_id).order_by(Document.id).offset(0).limit(100).all()
        return documents

    @staticmethod
    def get_document_by_id(user_id:str, id: str) -> Optional[Document]:
        document = Document.query.filter_by(user_id=user_id, id=id).first()
        return document

    @staticmethod
    def get_document_content(document_path:str) -> Optional[bytes]:
        import os, pathlib
        path = pathlib.Path(document_path)
        
        if not path.exists():
            return None
        
        with open(path, "rb") as f:
            return f.read()


    @staticmethod
    def store_document_file(user_id: str, file_content) -> Tuple[bool, str, str]:
        import os, pathlib
        import hashlib
 
        path = pathlib.Path('local_storage', user_id)
        if not path.exists():
            os.mkdir(path)

        document_hash = hashlib.sha256(file_content).hexdigest()

        path = path.joinpath(document_hash)
        if path.exists():   
            return False, document_hash, str(path)

        with open(path, "wb") as f:
            f.write(file_content)

        return True, document_hash, str(path)


    @staticmethod
    def create_document(user_id: str, file_name: str, file_hash: str, storage_path: str) -> Document:
        id = uuid.uuid4().hex
        document = Document(
            id=id,
            user_id=user_id,
            file_name=file_name,
            document_hash=file_hash,
            document_path=storage_path,
        )
        db.session.add(document)
        db.session.commit()

        return document
