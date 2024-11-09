
import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.check import blp as DatabaseCheck
from db import db
import models
import secrets

def create_app(db_url=None):
    app = Flask(__name__)

    # Configuration for Flask and Swagger
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = ""
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # Remote repository
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Debug mode setting
    app.config["DEBUG"] = True

    # Initialize API with Flask app
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "viltor"
    jwt = JWTManager(app)

    with app.app_context():
        print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])  # Debugging line
        db.create_all()
        print("Database tables created")  # Confirm this line is reached

    # Register blueprints for routes
    app.register_blueprint(ItemBlueprint)
    app.register_blueprint(StoreBlueprint)
    app.register_blueprint(TagBlueprint)
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(DatabaseCheck)

    return app

    # Only run if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)