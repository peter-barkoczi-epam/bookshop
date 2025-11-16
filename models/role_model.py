from database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import models.user_model as user_model

class Role(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    users = relationship(user_model.User, back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"