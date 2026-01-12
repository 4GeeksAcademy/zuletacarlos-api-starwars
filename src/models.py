from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(50))
    gender = db.Column(db.String(50))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(
        db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(
        db.Integer, db.ForeignKey('people.id'), nullable=True)

    user = db.relationship('User', backref='favorites')
    planet = db.relationship('Planet')
    people = db.relationship('People')

    def serialize(self):
        return {
            "id": self.id,
            "user_email": self.user.email if self.user else None,
            "planet_name": self.planet.name if self.planet else None,
            "people_name": self.people.name if self.people else None,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
