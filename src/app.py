
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

# ENDPOINTS PARA PEOPLE


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    results = list(map(lambda item: item.serialize(), all_people))
    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        raise APIException('People not found', status_code=404)
    return jsonify(people.serialize()), 200

# ENDPOINTS PARA PLANETS


@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    results = list(map(lambda item: item.serialize(), all_planets))
    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

# ENDPOINTS PARA USERS


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    results = list(map(lambda item: item.serialize(), all_users))
    return jsonify(results), 200


def get_current_user():
    return User.query.first()


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user = get_current_user()
    if not current_user:
        raise APIException('User not found', status_code=404)

    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    results = list(map(lambda item: item.serialize(), favorites))
    return jsonify(results), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user = get_current_user()
    planet = Planet.query.get(planet_id)
    if not planet:
        raise APIException('Planet not found', status_code=404)

    # Verificar si ya es favorito
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id, planet_id=planet_id).first()
    if existing_favorite:
        raise APIException('Planet already in favorites', status_code=400)

    new_favorite = Favorite(user_id=current_user.id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    current_user = get_current_user()
    people = People.query.get(people_id)
    if not people:
        raise APIException('People not found', status_code=404)

    # Verificar si ya es favorito
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id, people_id=people_id).first()
    if existing_favorite:
        raise APIException('People already in favorites', status_code=400)

    new_favorite = Favorite(user_id=current_user.id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = get_current_user()
    favorite_to_delete = Favorite.query.filter_by(
        user_id=current_user.id, planet_id=planet_id).first()

    if not favorite_to_delete:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite_to_delete)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted successfully"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    current_user = get_current_user()
    favorite_to_delete = Favorite.query.filter_by(
        user_id=current_user.id, people_id=people_id).first()

    if not favorite_to_delete:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite_to_delete)
    db.session.commit()
    return jsonify({"msg": "Favorite people deleted successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
