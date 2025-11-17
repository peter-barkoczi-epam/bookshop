from authenticator import auth
from services.book_store_service import BookStoreService

class BookStoreController:

    @staticmethod
    def get(book_store_item_id: int):
        return BookStoreService.get(book_store_item_id)

    @staticmethod
    # @auth.login_required
    def get_all():
        return BookStoreService.get_all()
    
    @staticmethod
    def create():
        return BookStoreService.create()
    
    @staticmethod
    def delete(book_store_item_id: int):
        return BookStoreService.delete(book_store_item_id)
    
    @staticmethod
    def update(book_store_item_id: int):
        return BookStoreService.update(book_store_item_id)
