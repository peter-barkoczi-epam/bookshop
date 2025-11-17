from database import db
from models.book_store_model import BookStore
from typing import List

class BookStoreDao:

    STORE_ITEM_NOT_FOUND = "Store item not found for id: {}"

    @staticmethod
    def create(book_store_item_id: BookStore):
        db.session.add(book_store_item_id)
        db.session.commit()

    @staticmethod
    def fetch_by_id(book_store_item_id: int) -> BookStore:
        return BookStore.query.get_or_404(
            book_store_item_id,
            description=BookStoreDao.STORE_ITEM_NOT_FOUND.format(book_store_item_id)
        )
    
    @staticmethod
    def fetch_all() -> List[BookStore]:
        return BookStore.query.all()
    
    @staticmethod
    def delete(book_store_item_id: int) -> None:
        item = BookStore.query.filter_by(id=book_store_item_id).first()
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update(book_store_data):
        db.session.merge(book_store_data)
        db.session.commit()
