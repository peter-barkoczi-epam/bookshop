from database import db
from dependencies import ma
from models.book_store_model import BookStore
from schemas.product_schema import ProductSchema
from marshmallow import fields

class BookStoreItemSchema(ma.SQLAlchemySchema):

    class Meta:
        model = BookStore
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    product_id = ma.auto_field()
    available_qty = ma.auto_field()
    booked_qty = ma.auto_field()
    sold_qty = ma.auto_field()
    product = fields.Nested(ProductSchema, dump_only=True)

