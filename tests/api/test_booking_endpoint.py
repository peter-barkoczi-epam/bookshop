from database import db
from models.bookings_model import Booking
from tests.factories import BookingFactory, UserFactory, ProductFactory

def add_user_to_db():
    user = UserFactory.build(login="admin")
    user.hash_password("adminpass")
    db.session.add(user)
    db.session.commit()
    return user

def add_product_to_db():
    product = ProductFactory.build(name="test_product", price=29.99)
    db.session.add(product)
    db.session.commit()
    return product

def test_create_booking(client, app_ctx, db, auth_header):
    user = add_user_to_db()
    product = add_product_to_db()
    payload = BookingFactory.create_payload(user_id=user.id, product_id=product.id)
    payload.pop('user', None)
    payload.pop('product', None)
    headers = auth_header("admin", "adminpass")
    resp = client.post("/api/booking", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 201
    assert data['id'] == 1
    assert data['user_id'] == user.id
    assert data['product_id'] == product.id

def test_get_all_bookings(client, app_ctx, db, auth_header):
    user = add_user_to_db()
    product = add_product_to_db()
    for x in range(3):    
        booking = BookingFactory.build(user_id=user.id, product_id=product.id)
        db.session.add(booking)
        db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get("/api/booking", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data[0]['user_id'] == user.id
    assert len(data) == 3

def test_get_booking_by_id(client, app_ctx, db, auth_header):   
    user = add_user_to_db()
    product = add_product_to_db()
    booking = BookingFactory.build(user_id=user.id, product_id=product.id)
    db.session.add(booking)
    db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get(f"/api/booking/{booking.id}", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['user_id'] == user.id
    assert data['id'] == booking.id

def test_delete_booking(client, app_ctx, db, auth_header):
    user = add_user_to_db()
    product = add_product_to_db()
    booking = BookingFactory.build(user_id=user.id, product_id=product.id)
    db.session.add(booking)
    db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.delete(f"/api/booking/{booking.id}", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 201
    assert data['message'] == 'Booking deleted successfully'

def test_update_booking(client, app_ctx, db, auth_header):
    user = add_user_to_db()
    product = add_product_to_db()
    booking = BookingFactory.build(user_id=user.id, product_id=product.id, delivery_address="Initial delivery_address")
    db.session.add(booking)
    db.session.commit()

    delivery_address = "Updated delivery_address"
    payload = {
        "delivery_address": delivery_address
    }

    headers = auth_header("admin", "adminpass")
    resp = client.put(f"/api/booking/{booking.id}", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['id'] == booking.id
    assert data['delivery_address'] == delivery_address