from sqlalchemy import Column, Integer, String, Boolean

from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(String(256))
    full_name = Column(String(256))
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(512))
    access_token = Column(String(512))
    google_access_token = Column(String(512))

    def __repr__(self):
       return f"<User(user_id='{self.user_id}', full_name='{self.full_name}', first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}'"
    
    def to_dict(self, sensitive=False):
        res = {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
            
        }

        if sensitive:
            res["access_token"] = self.access_token
            res["google_access_token"] = self.google_access_token
        
        return res
