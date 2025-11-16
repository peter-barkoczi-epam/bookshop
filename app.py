from flask import Flask
import connexion
from config import get_environment_config
from database import db
from dependencies import ma
import routes.user_route as user_routes


def create_app() -> Flask:

    # options = {'swagger_ui': True}
    # connexion_app = connexion.FlaskApp(__name__,
    #                               specification_dir='./openapi/',
    #                               swagger_ui_options=options)
    # connexion_app.add_api('swagger.yml')
    # application = connexion_app.app
    application = Flask(__name__)
    application.config.from_object(get_environment_config())

    db.init_app(application)
    ma.init_app(application)

    with application.app_context():
        db.create_all()
        return application


def add_routes(application):

    application.add_url_rule("/user", methods=["GET", "POST"], view_func=user_routes.user_control)
    application.add_url_rule("/user/<int:user_id>", methods=["GET", "PUT", "DELETE"], view_func=user_routes.user_manipulation)

app = create_app()

if __name__ == "__main__":
    add_routes(app)
    app.run()
    
