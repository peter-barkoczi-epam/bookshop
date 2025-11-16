from flask_httpauth import HTTPBasicAuth

from models.user_model import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login, password):
    user = User.query.filter_by(login=login).first()
    if not user or not user.verify_password(password):
        return False
    return True