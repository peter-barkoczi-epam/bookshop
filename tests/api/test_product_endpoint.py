from database import db
from models.products_model import Product
from tests.factories import ProductFactory, UserFactory

def add_user_to_db():
    user = UserFactory.build(login="admin")
    user.hash_password("adminpass")
    db.session.add(user)
    db.session.commit()
    return user

def test_create_product(client, app_ctx, db, auth_header):
    add_user_to_db()
    payload = ProductFactory.create_payload(name="created_product", price=19.99)
    headers = auth_header("admin", "adminpass")
    resp = client.post("/api/product", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 201
    assert data['id'] == 1
    assert data['name'] == 'created_product'
    assert data['price'] == 19.99

def test_get_all_products(client, app_ctx, db, auth_header):
    add_user_to_db()
    for x in range(3):    
        product = ProductFactory.build(name="intproduct"+str(x))
        db.session.add(product)
        db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get("/api/product", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert isinstance(data, list)
    assert data[0]['name'] == 'intproduct0'
    assert len(data) == 3

def test_get_product_by_id(client, app_ctx, db, auth_header):
    add_user_to_db()
    product = ProductFactory.build(name="intproduct2")
    db.session.add(product)
    db.session.commit()

    headers = auth_header("admin", "adminpass")
    resp = client.get(f"/api/product/{product.id}", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['name'] == 'intproduct2'
    assert data['id'] == product.id

def test_delete_product(client, app_ctx, db, auth_header):
    add_user_to_db()
    product = ProductFactory.build(name="tobedeleted")
    db.session.add(product)
    db.session.commit()
    headers = auth_header("admin", "adminpass")
    resp = client.delete(f"/api/product/{product.id}", headers=headers)
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['message'] == 'Product deleted successfully'

def test_update_product(client, app_ctx, db, auth_header):
    add_user_to_db()
    product = ProductFactory.build(name="tobeupdated", price=9.99)
    db.session.add(product)
    db.session.commit()

    headers = auth_header("admin", "adminpass")
    update_payload = {
        "name": "updated_product",
        "price": 14.99
    }
    resp = client.put(f"/api/product/{product.id}", json=update_payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['name'] == 'updated_product'
    assert data['price'] == 14.99