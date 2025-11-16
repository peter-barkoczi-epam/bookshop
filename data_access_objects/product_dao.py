from database import db
from models.products_model import Product
from typing import List

class ProductDao:

    PRODUCT_NOT_FOUND = "Product not found for id: {}"

    @staticmethod
    def create(product: Product):
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def fetch_by_id(product_id: int) -> Product:
        return Product.query.get_or_404(
            product_id,
            description=ProductDao.PRODUCT_NOT_FOUND.format(product_id)
        )
    
    @staticmethod
    def fetch_all() -> List[Product]:
        return Product.query.all()
    
    @staticmethod
    def delete(product_id: int) -> None:
        item = Product.query.filter_by(id=product_id).first()
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update(product_data):
        db.session.merge(product_data)
        db.session.commit()
