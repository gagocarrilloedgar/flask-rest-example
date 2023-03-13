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
from models import db, User, Civilization, Category, Character

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
    users = list(map(lambda x: x.serialize(), users))

    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def add_user():
    user = User()

    request_user = request.json

    user.email = request.json.get("email", None)
    user.password = request_user["password"]

    # Here we should add password encrypton

    user.is_active = True

    db.session.add(user)
    db.session.commit()

    response = {
        "msg": "User successfully created"
    }

    return jsonify(response), 201


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/check", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_email = get_jwt_identity()
    user = User.query.filter_by(email=current_email).first()

    return jsonify(user.serialize()), 200


@app.route("/categories", methods=["POST"])
def add_category():

    title = request.json.get("title", None)

    newCategory = Category(title=title)

    db.session.add(newCategory)
    db.session.commit()

    response = {
        "msg": "Category successfully created"
    }

    return jsonify(response), 201


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True


@app.route("/categories", methods=["GET"])
def get_categories():

    categories = Category.query.all()
    categories_schema = CategoriesSchema(many=True)
    output = categories_schema.dump(categories)

    return output, 200


class CivilizationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Civilization
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()


@app.route("/civilizations", methods=["GET"])
def get_civilzations():

    civilization = Civilization.query.first()
    civilization_schema = CivilizationSchema()
    output = civilization_schema.dump(civilization)
    return jsonify(output)


@app.route("/civilizations", methods=["POST"])
def add_civilization():

    name = request.json.get("name", None)

    newCivilization = Civilization(name=name)

    db.session.add(newCivilization)
    db.session.commit()

    response = {
        "msg": "Civilization successfully created"
    }

    return jsonify(response), 201


@app.route("/characters", methods=["POST"])
def add_character():

    name = request.json.get("name", None)
    category_id = request.json.get("category_id", None)
    newCharacter = Character(name=name, category_id=category_id)

    db.session.add(newCharacter)
    db.session.commit()

    response = {
        "msg": "Character successfully created"
    }

    return jsonify(response), 201


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        include_fk = True

    category_id = ma.auto_field()
    category = ma.Nested(CategoriesSchema)


@app.route("/characters", methods=["GET"])
def get_characters():

    characters = Character.query.all() # If we have the lazy attached to the relationship -> we will get category automatically
    characters_schema = CharacterSchema(many=True)
    output = characters_schema.dump(characters)

    

    return output, 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3002))
    app.run(host='0.0.0.0', port=PORT, debug=False)


"""
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
"""
