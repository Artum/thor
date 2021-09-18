from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func

from database import db

class Document(db.Model):
    __tablename__ = 'document'

    id = Column(String(256), primary_key=True)
    user_id = Column(String(256))
    file_name = Column(String(256))
    document_hash = Column(String(256))
    document_path = Column(String(256))

    def __repr__(self):
       return f"<Document(id='{self.id}', user_id='{self.user_id}', file_name='{self.file_name}', document_hash='{self.document_hash}', document_path='{self.document_path}')>"
    
    def to_dict(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "file_name": self.file_name,
            "document_hash": self.document_hash,
            "document_path": self.document_path,
        }
