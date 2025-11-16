from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from data_access_objects.product_dao import ProductDao
from schemas.product_schema import ProductSchema

productSchema = ProductSchema()
productListSchema = ProductSchema(many=True)

class ProductService:
    
    @staticmethod
    def get(product_id: int):
        product_data = ProductDao.fetch_by_id(product_id)
        return productSchema.dump(product_data)
    
    @staticmethod
    def get_all():
        return productListSchema.dump(ProductDao.fetch_all())
    
    @staticmethod
    def create():
        product_req_json = request.get_json()
        product_data = productSchema.load(product_req_json)
        ProductDao.create(product_data)
        return productSchema.dump(product_data), 201
    
    @staticmethod
    def delete(product_id: int):
        ProductDao.fetch_by_id(product_id)
        ProductDao.delete(product_id)
        return {'message': 'Product deleted successfully'}, 201
    
    @staticmethod
    def update(product_id: int):
        try:
            product_data = productSchema.dump(ProductDao.fetch_by_id(product_id))
            product_data.update(request.get_json())
            product_data = productSchema.load(product_data)
            ProductDao.update(product_data)
            return productSchema.dump(product_data), 404
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")
