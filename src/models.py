from flask_sqlalchemy import SQLAlchemy

# For serializations
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", lazy=True)

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


civilazations = db.Table('civilizations',
                         db.Column('character_id', db.Integer, db.ForeignKey(
                             'character.id')),
                         db.Column('civilization_id', db.Integer, db.ForeignKey(
                             'civilization.id')))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    characters = db.relationship("Character", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __repr__(self):
        return '<Category %r>' % self.title



class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    civilizations = db.relationship(
        'Civilization', secondary=civilazations)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f'id: "{str(self.id)}",  civilizations : "{str(self.civilizations)}"'


class Civilization(db.Model):
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


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    character_id = db.Column(db.Integer, db.ForeignKey(Character.id))

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
