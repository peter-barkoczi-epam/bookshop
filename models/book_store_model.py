from database import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class BookStore(db.Model):
    __tablename__ = "book_store"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    available_qty = Column(Integer, nullable=False)
    booked_qty = Column(Integer, nullable=False)
    sold_qty = Column(Integer, nullable=False)
    product = relationship("Product", back_populates="book_stores")

    def __repr__(self) -> str:
        return f"<BookStore {self.id}>"
