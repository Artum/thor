from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func

from database import db

class Document(db.Model):
    __tablename__ = 'document'

    id = Column(String(256), primary_key=True)
    user_id = Column(String(256))

    def __repr__(self):
       return f"<Invoice(id='{self.id}', user_id='{self.user_id}')>"
    
    def to_dict(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
        }
