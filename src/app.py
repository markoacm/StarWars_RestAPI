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
from models import db, User, People, Planets
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



# Endpoints

# //////GET Requests///////

@app.route('/user', methods=['GET'])
def get_user():

  users = User.query.all()
  user_data = []
  for user in users:
      user_data.append(user.serialize())

  return jsonify(user_data), 200


@app.route('/people', methods=['GET'])
def get_people():

    people_info= People.query.all()
    people_data = []
    for people in people_info:
        people_data.append(people.serialize())

    return jsonify(people_data), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_detail(people_id):
    
    person_detail = People.query.get(people_id)
    if person_detail:
        person = person_detail.serialize()
        return jsonify(person), 200
    else:
        return jsonify({"Message":"Person does not exist"})


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    planets_data = []
    for planet in planets:
        planets_data.append(planet.serialize())

    return jsonify(planets_data), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_detail(planet_id):

    planet_detail = Planets.query.get(planet_id)
    if planet_detail:
        planet = planet_detail.serialize()
        return jsonify(planet), 200
    else:
        return jsonify({"Message":"Planet does not exist"})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
