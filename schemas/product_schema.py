from database import db
from dependencies import ma
from models.products_model import Product

class ProductSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Product
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    author = ma.auto_field()
    price = ma.auto_field()
    image_path = ma.auto_field()