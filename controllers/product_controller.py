from authenticator import auth
from services.product_service import ProductService

class ProductController:

    @staticmethod
    def get(product_id: int):
        return ProductService.get(product_id)

    @staticmethod
    # @auth.login_required
    def get_all():
        return ProductService.get_all()
    
    @staticmethod
    def create():
        return ProductService.create()
    
    @staticmethod
    def delete(product_id: int):
        return ProductService.delete(product_id)
    
    @staticmethod
    def update(product_id: int):
        return ProductService.update(product_id)
