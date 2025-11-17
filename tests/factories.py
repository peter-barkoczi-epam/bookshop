from typing import Dict
from models.user_model import User
from models.role_model import RoleEnum
from models.products_model import Product
from models.bookings_model import Booking
from models.book_store_model import BookStore
import datetime
from schemas.user_schema import UserSchema


class UserFactory:
    _id_counter = 1

    @classmethod
    def build(cls, **overrides) -> User:
        if 'id' not in overrides:
            overrides['id'] = cls._id_counter
            cls._id_counter += 1

        defaults = {
            'name': f"Test User {overrides.get('id')}",
            'role_id': RoleEnum.CUSTOMER.value,
            'email': f"user{overrides.get('id')}@example.com",
            'phone': '000-000',
            'address': 'test address',
            'login': f"test{overrides.get('id')}"
        }
        data = {**defaults, **overrides}

        return User(**data)

    @staticmethod
    def dump(user: User) -> Dict:
        schema = UserSchema()
        return schema.dump(user)

    @classmethod
    def create_payload(cls, **overrides) -> Dict:
        user = cls.build(**overrides)
        return cls.dump(user)


class ProductFactory:
    _id_counter = 1

    @classmethod
    def build(cls, **overrides):
        if 'id' not in overrides:
            overrides['id'] = cls._id_counter
            cls._id_counter += 1

        defaults = {
            'name': f"Test Product {overrides.get('id')}",
            'description': 'A sample product description',
            'price': 9.99,
            'author': 'Test Author',
            'image_path': '/path/to/image.jpg'
        }
        data = {**defaults, **overrides}

        return Product(**data)

class BookingFactory:
    _id_counter = 1

    @classmethod
    def build(cls, **overrides):
        if 'id' not in overrides:
            overrides['id'] = cls._id_counter
            cls._id_counter += 1

        defaults = {
            'user_id': 1,
            'product_id': 1,
            'delivery_address': '123 Test St, Test City',
            'delivery_date': datetime.date(2024, 12, 31),
            'delivery_time': datetime.datetime(2024, 12, 31, 14, 0),
            'status_id': 1,
            'quantity': 1
        }
        data = {**defaults, **overrides}

        return Booking(**data)

class BookStoreItemFactory:
    _id_counter = 1

    @classmethod
    def build(cls, **overrides):
        if 'id' not in overrides:
            overrides['id'] = cls._id_counter
            cls._id_counter += 1

        defaults = {
            'product_id': 1,
            'available_qty': 12,
            'booked_qty': 12,
            'sold_qty': 2
        }
        data = {**defaults, **overrides}

        return BookStore(**data)

__all__ = ['UserFactory', 'ProductFactory', 'BookingFactory']