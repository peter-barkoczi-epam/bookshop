import enum
from database import db
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import relationship

class RoleEnum(enum.Enum):
    ADMIN = 1
    MANAGER = 2
    CUSTOMER = 3

class Role(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"
    
@event.listens_for(Role.__table__, 'after_create')
def create_roles(*args, **kwargs):
    db.session.add(Role(id=RoleEnum.ADMIN.value, name=str(RoleEnum.ADMIN.name)))
    db.session.add(Role(id=RoleEnum.MANAGER.value, name=str(RoleEnum.MANAGER.name)))
    db.session.add(Role(id=RoleEnum.CUSTOMER.value, name=str(RoleEnum.CUSTOMER.name)))
    db.session.commit()