from database import db
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"
    
@event.listens_for(Role.__table__, 'after_create')
def create_roles(*args, **kwargs):
    db.session.add(Role(id=1, name="Admin"))
    db.session.add(Role(id=2, name="Manager"))
    db.session.add(Role(id=3, name="Customer"))
    db.session.commit()