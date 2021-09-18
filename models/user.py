from sqlalchemy import Column, Integer, String, Boolean

from database import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = Column(String(256), primary_key=True)
    full_name = Column(String(256))
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(512))
    token = Column(String(512))

    def __repr__(self):
       return f"<User(user_id='{self.user_id}', full_name='{self.full_name}', first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', token='*****')>"
    
    def to_dict(self, sensitive=False):
        res = {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
            
        }

        if sensitive:
            res["token"] = self.token
        
        return res
