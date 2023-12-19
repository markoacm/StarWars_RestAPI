from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birth_year = db.Column(db.String)
    weight = db.Column(db.String)
    height = db.Column(db.String)
    gender = db.Column(db.String)
    eye_color = db.Column(db.String)
    hair_color = db.Column(db.String)

    def serialize(self):
         return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "weight": self.weight,
            "height": self.height,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,

        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    diameter = db.Column(db.String)
    gravity = db.Column(db.String)
    terrain = db.Column(db.String)
    climate = db.Column(db.String)

    def serialize(self):
         return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "climate": self.climate,

        }



class Favorite_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey(People.id), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "people": self.people_id,
        }



class Favorite_Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey(Planets.id), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planets": self.planets_id,
        }


    








