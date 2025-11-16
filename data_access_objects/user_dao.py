from database import db
from models.user_model import User
from typing import List

class UserDao:

    USER_NOT_FOUND = "User not found for id: {}"

    @staticmethod
    def create(user: User):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def fetch_by_id(user_id: int) -> User:
        return User.query.get_or_404(
            user_id,
            description=UserDao.USER_NOT_FOUND.format(user_id)
        )
    
    @staticmethod
    def fetch_all() -> List[User]:
        return User.query.all()
    
    @staticmethod
    def delete(user_id: int) -> None:
        item = User.query.filter_by(id=user_id).first()
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update(user_data):
        db.session.merge(user_data)
        db.session.commit()
