
import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.check import blp as DatabaseCheck
from blocklist import BLOCKLIST
from flask_migrate import Migrate
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

    migrate = Migrate(app, db)

    # Debug mode setting
    app.config["DEBUG"] = True

    # Initialize API with Flask app
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "viltor"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "Token has been revoked",
                     "error": "token revoked"})
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                    "description": "The token is not fresh",
                    "error": "fresh token required"}),
                401
        )


    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see wether the user is an admin
        if identity == 1:
            return {"is admin": True}
        return {"is admin": False}


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired", "error": "token expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature varification failed", "error": "invalid token"}),
            401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token",
                     "error": "authorisation required"})
        )

    # Register blueprints for routes
    app.register_blueprint(ItemBlueprint)
    app.register_blueprint(StoreBlueprint)
    app.register_blueprint(TagBlueprint)
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(DatabaseCheck)

    @app.route("/")
    def hello():
        return {"message": "Hello, World!"}

    return app

    # Only run if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)