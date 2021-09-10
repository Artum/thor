from typing import Optional
from models.user import User
from database import db

class UserService:

    @staticmethod
    def get_user_access_token(user: User) -> str:
        return user.token

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        user = User.query.filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def create_user(user_id: str, access_token: str, user_full_name: str, user_first_name: str, user_last_name: str, user_email: str) -> User:
        user = User(
            token=access_token,
            user_id=user_id,
            full_name=user_full_name,
            first_name=user_first_name,
            last_name=user_last_name,
            email=user_email
        )
        db.session.add(user)
        db.session.commit()

        return user
    
    @staticmethod
    def update_access_token(user: User, access_token: str):
        user.token = access_token
        db.session.add(user)
        db.session.commit()