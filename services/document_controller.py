from models.document import Document
from typing import Iterable, Optional


class DocumentController:

    @staticmethod
    def get_all_documents(user_id: str) -> Iterable[Document]:
       return [Document(id=i,user_id=user_id) for i in range(100)]

    @staticmethod
    def get_document_by_id(id: str) -> Optional[Document]:
        return None