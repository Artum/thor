from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    full_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    auth_code = Column(String(255))
    is_active = Column(Boolean())

    def __repr__(self):
       return f"<User(full_name='{self.full_name}', first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', is_active='{self.is_active}'"
    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "auth_code": self.auth_code,
            "is_active": self.is_active
        }