from database import db
from models.user_model import User
from models.role_model import RoleEnum
from tests.factories import UserFactory


def test_create_user(client, app_ctx, db, auth_header):
    payload = UserFactory.create_payload(login="created_user")
    payload['password'] = 'create_pass'
    del payload['role']
    headers = auth_header("created_user", "create_pass")
    resp = client.post("/api/user", json=payload, headers=headers)

    data = resp.get_json()
    assert resp.status_code == 201
    assert data['id'] == 1
    assert data['login'] == 'created_user'

def test_get_all_users(client, app_ctx, db, auth_header):
    for x in range(3):    
        user = UserFactory.build(login="intuser"+str(x))
        user.hash_password("secret")
        db.session.add(user)
        db.session.commit()

    headers = auth_header("intuser1", "secret")
    resp = client.get("/api/user", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert isinstance(data, list)
    assert data[0]['login'] == 'intuser0'
    assert len(data) == 3

def test_get_user_by_id(client, app_ctx, db, auth_header):
    user = UserFactory.build(login="intuser2")
    user.hash_password("secret2")
    db.session.add(user)
    db.session.commit()

    headers = auth_header("intuser2", "secret2")
    resp = client.get(f"/api/user/{user.id}", headers=headers)

    data = resp.get_json()
    assert resp.status_code == 200
    assert data['login'] == 'intuser2'
    assert data['id'] == user.id

def test_delete_user(client, app_ctx, db, auth_header):
    user = UserFactory.build(login="tobedeleted")
    user.hash_password("deletepass")
    db.session.add(user)
    db.session.commit()
    headers = auth_header("tobedeleted", "deletepass")
    resp = client.delete(f"/api/user/{user.id}", headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['message'] == 'User deleted successfully'

def test_update_user(client, app_ctx, db, auth_header):
    user = UserFactory.build(login="tobeupdated")
    user.hash_password("updatepass")
    db.session.add(user)
    db.session.commit()

    headers = auth_header("tobeupdated", "updatepass")
    payload = {
        "address": "new address",
        "role_id": RoleEnum.ADMIN.value,
    }
    resp = client.put(f"/api/user/{user.id}", json=payload, headers=headers)
    assert resp.status_code == 200

    updated_user = User.query.get(user.id)
    assert updated_user.address == "new address"
    assert updated_user.login == "tobeupdated"
    assert updated_user.role_id == RoleEnum.ADMIN.value