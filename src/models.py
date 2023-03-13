from flask_sqlalchemy import SQLAlchemy

# For serializations
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref=db.backref(
        'favorites', uselist=True), lazy=True, uselist=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def listausuarios(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
        }

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


civilazations = db.Table('civilizations_types',
                         db.Column('character_id', db.Integer, db.ForeignKey(
                             "characters.id")),
                         db.Column('civilization_id', db.Integer, db.ForeignKey(
                             "civilizations.id")))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    characters = db.relationship('Character', backref=db.backref(
        'characters', uselist=True), lazy=True, uselist=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __repr__(self):
        return '<Category %r>' % self.title


class Civilization(db.Model):
    __tablename__ = "civilizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Civilization %r>' % self.name

    def list_all(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        Category.id), unique=True, nullable=False)

    category = db.relationship('Category', backref=db.backref(
        'categories'), lazy=True)

    civilizations = db.relationship(
        'Civilization', secondary=civilazations)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f'id: "{str(self.id)}",  civilizations : "{str(self.civilizations)}"'


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
