"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
https://flask-marshmallow.readthedocs.io/en/latest/
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Planet, Civilization

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


ma = Marshmallow(app)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda x: x.listausuarios(), users))

    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def add_user():
    user = User()

    request_user = request.json

    user.email = request.json.get("email", None)
    user.password = request_user["password"]
    user.is_active = True

    user_id = request.json.get("user_id", None)
    print(user_id)

    db.session.add(user)
    db.session.commit()

    response = {
        "msg": "User successfully created"
    }

    return jsonify(response), 201

    # this only runs if `$ python src/main.py` is executed


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/favorites", methods=["GET"])
def get_favorites():

    favorites = Favorites.query.all()
    favorites = list(map(lambda x: x.serialize(), favorites))

    return jsonify(favorites), 200


@app.route("/favorites", methods=["POST"])
def add_favorite():

    # Create a new instace of the class
    favorite = Favorites()

    # Save the info inside the class parameters
    favorite.user_id = request.json.get("user_id", None)
    favorite.planets_id = request.json.get("planets_id", None)

    # Add the information to the database
    db.session.add(favorite)

    # Finally we commit the operation
    db.session.commit()

    return jsonify(message="ok"), 200


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


class PlanetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Planet

    id = ma.auto_field()
    # civilizations = ma.List(ma.HyperlinkRelated("get_civilzations"))
    civilizations = ma.auto_field()


@ app.route("/planets", methods=["GET"])
def get_planets():

    planet = Planet.query.first()
    planet_schema = PlanetSchema()
    output = planet_schema.dump(planet)
    return jsonify(output)


class CivilizationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Civilization

    id = ma.auto_field()
    name = ma.auto_field()


@ app.route("/civilization", methods=["GET"])
def get_civilzations():

    civilization = Civilization.query.first()
    civilization_schema = CivilizationSchema()
    output = civilization_schema.dump(civilization)
    return jsonify(output)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3002))
    app.run(host='0.0.0.0', port=PORT, debug=False)
