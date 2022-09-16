from flask_sqlalchemy import SQLAlchemy

# For serializations
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

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
                         db.Column('planet_id', db.Integer, db.ForeignKey(
                             'planet.id')),
                         db.Column('civilization_id', db.Integer, db.ForeignKey(
                             'civilization.id')))


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    civilizations = db.relationship(
        'Civilization', secondary=civilazations, backref='plantes')

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


class Favorites(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship("User")
    planet = db.relationship('Planet')

    def repr(self):
        return '<Favorites %r>' % self.id

    def serialize(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
        }
