"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


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

    user.email = request_user["email"]
    user.password = request_user["password"]
    user.is_active = True

    db.session.add(user)
    db.session.commit()

    response = {
        "msg": "User successfully created"
    }

    return jsonify(response), 201

    # this only runs if `$ python src/main.py` is executed


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3002))
    app.run(host='0.0.0.0', port=PORT, debug=False)
