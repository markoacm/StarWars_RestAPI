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
from models import db, User, People, Planets, Favorite_People, Favorite_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False



db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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



# ////////ENPOINTS/////////

# //////GET Requests///////

@app.route('/user', methods=['GET'])
def get_users():

  users = User.query.all()
  user_data = []
  for user in users:
      user_data.append(user.serialize())

  return jsonify(user_data), 200


@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()
    return jsonify({'people': [person.serialize() for person in people]})

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character_detail(people_id):

    character = People.query.get(people_id)
    if character:
        return jsonify(character.serialize())
    else:
        return jsonify({'Message': 'Character not found'}), 404


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    return jsonify({'planets': [planet.serialize() for planet in planets]})


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_detail(planet_id):

    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    else:
        return jsonify({'Message': 'Planet not found'}), 404


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1

    favorite_people = Favorite_People.query.filter_by(user_id=user_id).all()
    favorite_planets = Favorite_Planets.query.filter_by(user_id=user_id).all()

    user_favorites = {
        'favorite_people': [favorite_character.serialize() for favorite_character in favorite_people],
        'favorite_planets': [favorite_planet.serialize() for favorite_planet in favorite_planets],
    }

    return jsonify({'user_favorites': user_favorites})


# //////POST Requests///////

@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()

    new_user = User(email=user_data['email'], password=user_data['password'], is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Message': 'User has been created successfully'}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()

    user_id = data['user_id']

    new_favorite_planet = Favorite_Planets(user_id=user_id, planets_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({'Message': 'Favorite Planet added successfully'}), 201
    

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.get_json()

    user_id = data['user_id']

    new_favorite_character = Favorite_People(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify({'Message': 'Favorite Character added successfully'}), 201




# //////DELETE Requests///////

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Message': 'User deleted successfully'})
    else:
        return jsonify({'Message': 'User not found'}), 404
    

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    data = request.get_json()

    user_id = data['user_id']

    favorite_planet = Favorite_Planets.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if not favorite_planet:
        return jsonify({'Message': 'Favorite planet not found'}), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    data = request.get_json()

    user_id = data['user_id']

    delete_favorite_character = Favorite_People.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not delete_favorite_character:
        return jsonify({'Message': 'Favorite Character not found'}), 404

    db.session.delete(delete_favorite_character)
    db.session.commit()

    return jsonify({'Message': 'Favorite Character deleted successfully'}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
