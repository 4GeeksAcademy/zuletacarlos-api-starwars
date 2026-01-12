import os
from flask import Flask, request, jsonify, url_for
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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    data = [person.serialize() for person in people]
    return jsonify(data), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200

# --- RUTAS DE PLANETAS ---


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    data = [planet.serialize() for planet in planets]
    return jsonify(data), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [user.serialize() for user in users]
    return jsonify(data), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorites = Favorite.query.all()
    data = [fav.serialize() for fav in favorites]
    return jsonify(data), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user_id = 1
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado (crea un usuario primero)"}), 404
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    # Verificar si ya existe
    existing = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if existing:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planeta añadido a favoritos"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    user_id = 1  # Usuario hardcodeado para pruebas

    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    if not person:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    existing = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if existing:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = 1
    fav = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Eliminado de favoritos"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    user_id = 1
    fav = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Eliminado de favoritos"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
