import os

from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


# Factory Pattern
def create_app(db_url = None):
    app = Flask(__name__)

    # In the first project, that is in rest_api_project, we generically defined a list which has stores
    # But practically, we would use a unique id, like UUID or a number (squence) for a unique record, here unique store
    # So now implementing those changes on the first project, also using flask-smorest, python-dotenv aditionally.
    # Eventhough smorest is also used to build rest apis, but this comes with more features, we get marshmallow, a python library used 
    # to easily serliaze and deserialze python objects into json and viceversa, helps us build production level application, and also comes
    # with auto openapi/ swagger documentation, that after we define all the routes, and if we search for /docs, the documentation would be ready
    #, everything automatically written. 

    # From our previous project, we are completely decoupling stores and items, like assigning individual ids to them, and properly storing them 
    # in db.py, and accessing these objects from db.py

    # Also, in first project, while returning, in the failure case, we were passing {"message": ""}, which is manual process, and since we are using 
    # flask-smorest, it auto generates the api documentation, and since we are manually handling by sending a dictionary as response {"message":}., we
    # will have to add that explicitly as well, to avoid this, flask-smorest provides a function called ABORT, which works in the same way, decreasing
    # manual effort.

    # The blueprints we have defined in the resources item and store, we will have to register them

    # Some necessary configuration

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    
    
    return app