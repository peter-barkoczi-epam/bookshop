from database import db
from models.book_store_model import BookStore
from tests.factories import BookStoreItemFactory, ProductFactory, UserFactory

def add_user_to_db():
    user = UserFactory.build(login="admin")
    user.hash_password("adminpass")
    db.session.add(user)
    db.session.commit()
    return user

def add_product_to_db():
    product = ProductFactory.build(name="store_product", price=39.99)
    db.session.add(product)
    db.session.commit()
    return product

def test_create_book_store_item(client, app_ctx, db, auth_header):
    product = add_product_to_db()
    payload = BookStoreItemFactory.create_payload(product_id=product.id, booked_qty=10)
    payload.pop('product', None)
    headers = auth_header("admin", "adminpass")
    resp = client.post("/api/book_store", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 201
    assert data['id'] == 1
    assert data['product_id'] == product.id
    assert data['booked_qty'] == 10

def test_get_all_book_store_items(client, app_ctx, db, auth_header):
    add_product_to_db()
    for x in range(3):    
        item = BookStoreItemFactory.build(booked_qty=5*(x+1))
        db.session.add(item)
        db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get("/api/book_store", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert isinstance(data, list)
    assert data[0]['booked_qty'] == 5
    assert len(data) == 3

def test_get_book_store_item_by_id(client, app_ctx, db, auth_header):   
    product = add_product_to_db()
    item = BookStoreItemFactory.build(product_id=product.id, booked_qty=15)
    db.session.add(item)
    db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get(f"/api/book_store/{item.id}", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['booked_qty'] == 15
    assert data['id'] == item.id

def test_delete_book_store_item(client, app_ctx, db, auth_header):
    product = add_product_to_db()
    item = BookStoreItemFactory.build(product_id=product.id, booked_qty=20)
    db.session.add(item)
    db.session.commit()
    headers = auth_header("admin", "adminpass")
    resp = client.delete(f"/api/book_store/{item.id}", headers=headers)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['message'] == 'Book store item deleted successfully'

def test_update_book_store_item(client, app_ctx, db, auth_header):
    product = add_product_to_db()
    item = BookStoreItemFactory.build(product_id=product.id, booked_qty=25)
    db.session.add(item)
    db.session.commit()
    headers = auth_header("admin", "adminpass")
    payload = {'booked_qty': 30}
    resp = client.put(f"/api/book_store/{item.id}", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['booked_qty'] == 30