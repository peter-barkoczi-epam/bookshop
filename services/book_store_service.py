from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from data_access_objects.book_store_dao import BookStoreDao
from schemas.store_item_schema import BookStoreItemSchema

bookStoreSchema = BookStoreItemSchema()
bookStoreListSchema = BookStoreItemSchema(many=True)

class BookStoreService:
    
    @staticmethod
    def get(store_item_id: int):
        book_store_data = BookStoreDao.fetch_by_id(store_item_id)
        return bookStoreSchema.dump(book_store_data)
    
    @staticmethod
    def get_all():
        return bookStoreListSchema.dump(BookStoreDao.fetch_all())
    
    @staticmethod
    def create():
        book_store_req_json = request.get_json()
        book_store_data = bookStoreSchema.load(book_store_req_json)
        BookStoreDao.create(book_store_data)
        return bookStoreSchema.dump(book_store_data), 201
    
    @staticmethod
    def delete(store_item_id: int):
        BookStoreDao.fetch_by_id(store_item_id)
        BookStoreDao.delete(store_item_id)
        return {'message': 'Book store item deleted successfully'}, 201
    
    @staticmethod
    def update(store_item_id: int):
        try:
            book_store_data = bookStoreSchema.dump(BookStoreDao.fetch_by_id(store_item_id))
            book_store_data.update(request.get_json())
            book_store_data = bookStoreSchema.load(book_store_data)
            BookStoreDao.update(book_store_data)
            return bookStoreSchema.dump(book_store_data), 404
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")
