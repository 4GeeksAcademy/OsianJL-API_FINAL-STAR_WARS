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
from models import db, User, Planets, Characters, Starships, Favorites
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
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

#DEFINIMOS NUESTROS ENDPOINTS:
#ENDPOINTS GET: 

@app.route('/user', methods=['GET'])
def get_all_users():
    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("no users in the database"), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }
    
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    query_results = Planets.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("no planets in the database"), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }
    
    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def get_all_characters():
    query_results = Characters.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("no characters in the database"), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }
    
    return jsonify(response_body), 200

@app.route('/starships', methods=['GET'])
def get_all_starships():
    query_results = Starships.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("no starships in the database"), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }
    
    return jsonify(response_body), 200

# ENDPOINTS PARA OBTENER USUARIOS, PLANETAS, PERSONAJES Y NAVES CONCRETAS, USANDO SU ID 

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    query_results = User.query.filter_by(id=user_id).first()
   

    if query_results is None:
        return jsonify({"msg": "there is no user matching the ID provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    query_results = Planets.query.filter_by(id=planets_id).first()
   

    if query_results is None:
        return jsonify({"msg": "there is no planet matching the ID provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):
    query_results = Characters.query.filter_by(id=characters_id).first()
   

    if query_results is None:
        return jsonify({"msg": "there is no character matching the ID provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200


# OBTENER TODOS LOS FAVORITOS DE UN USUARIO
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_all_favorites_of_user(user_id):
    query_results = Favorites.query.filter_by(user_id=user_id).all()
    

    if query_results:
        results = list(map(lambda item: item.serialize(), query_results))
        return jsonify({"msg": "ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "this user has no favorites yet"}), 404



# CREAR NUEVOS FAVORITOS PARA USUARIOS 

@app.route('/favorites/planet/<int:planets_id>', methods=['POST'])
def add_new_favorite_planet(planets_id):
    data = request.json
    print(data)

    user_exists = User.query.filter_by(id=data["user_id"]).first()
    planets_exists = Planets.query.filter_by(id=data["planets_id"]).first()
    
    if user_exists and planets_exists: 


        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], user_id=data["user_id"]).first()

        if query_results is None: 

            new_favorite = Favorites(planets_id=data["planets_id"], user_id=data["user_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200

       

        else:
            return ({"msg": "this user already has this planet as a favorite"}), 200
        
    elif user_exists is None and planets_exists is None:
        return ({"msg": "both user and planet do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif planets_exists is None: 
        return ({"msg": "this planet does not exist"}), 400
    

@app.route('/favorites/character/<int:characters_id>', methods=['POST'])
def add_new_favorite_character(characters_id):
    data = request.json
    print(data)

    user_exists = User.query.filter_by(id=data["user_id"]).first()
    characters_exists = Characters.query.filter_by(id=data["characters_id"]).first()
    
    if user_exists and characters_exists: 


        query_results = Favorites.query.filter_by(characters_id=data["characters_id"], user_id=data["user_id"]).first()

        if query_results is None: 

            new_favorite = Favorites(characters_id=data["characters_id"], user_id=data["user_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200

       

        else:
            return ({"msg": "this user already has this character as a favorite"}), 200
        
    elif user_exists is None and characters_exists is None:
        return ({"msg": "both user and character do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif characters_exists is None: 
        return ({"msg": "this character does not exist"}), 400    

 



# BORRAR UN PLANETA FAVORITO DE UNA CUENTA DE UN USUARIO
# PRIMER MÉTODO, USANDO EL REQUEST.JSON PARA SABER IDS DE USUARIO Y PLANETA
@app.route('/favorites/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    data = request.json

    user_exists = User.query.filter_by(id=data["user_id"]).first()
    planets_exists = Planets.query.filter_by(id=data["planets_id"]).first()
    
    if user_exists and planets_exists: 

        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], user_id=data["user_id"]).first()

        if query_results: 
         
            db.session.delete(query_results)
            db.session.commit()
            return ({"msg": "ok, its deleted"}), 200

        

        else: 

           return ({"msg": "there is nothing to delete"}), 200

       

# SEGUNDO MÉTODO, USANDO LA URL DINÁMICA PARA SABER IDS DE USUARIO Y PLANETA (METODO OPTIMO)        
@app.route('/favorites/character/<int:user_id>/<int:characters_id>', methods=['DELETE'])
def delete_favorite_character(user_id,characters_id):
   

    user_exists = User.query.filter_by(id=user_id).first()
    character_exists = Characters.query.filter_by(id=characters_id).first()
    
    if user_exists and character_exists: 

        query_results = Favorites.query.filter_by(characters_id=characters_id, user_id=user_id).first()

        if query_results: 
         
            db.session.delete(query_results)
            db.session.commit()
            return ({"msg": "ok, its deleted"}), 200

        

        else: 

           return ({"msg": "there is nothing to delete"}), 200

       



#CREAR UN PLANETA NUEVO
@app.route('/planet', methods=['POST'])
def add_new_planet():
    data = request.json
    print(data)

    planet_exists = Planets.query.filter_by(name=data["name"]).first()
    
    if planet_exists is None: 

            new_planet = Planets(
                name=data["name"], 
                climate=data["climate"], 
                population=data["population"], 
                orbital_period=data["orbital_period"], 
                rotation_period=data["rotation_period"], 
                diameter=data["diameter"]
                )
            db.session.add(new_planet)
            db.session.commit()
            return ({"msg": "ok, a new planet has been added to the database"}), 200

       

    else:
            return ({"msg": "this planet already is already included in the database"}), 200
        
# BORRAR PLANETAS EN BASE A SU NOMBRE        
@app.route('/planet', methods=['DELETE'])
def delete_planet():
    data = request.json

    
    planet_exists = Planets.query.filter_by(name=data["name"]).first()
    
    if planet_exists: 
         
            db.session.delete(planet_exists)
            db.session.commit()
            return ({"msg": "ok, its deleted"}), 200

        

    else: 

           return ({"msg": "there is nothing to delete"}), 200
    




# ACTUALIZAR DATOS DE UN PLANETA en base a su nombre
@app.route('/planet', methods=['PUT'])
def update_planet():
    data = request.json
    print(data)

    planet = Planets.query.filter_by(name=data["name"]).first()
    
    if planet: 
    
            planet.climate=data["climate"], 
            planet.population=data["population"], 
            planet.orbital_period=data["orbital_period"], 
            planet.rotation_period=data["rotation_period"], 
            planet.diameter=data["diameter"]
                
            
            db.session.commit()
            return ({"msg": "ok, the planet has been updated in the database"}), 200

       

    else:
            return ({"msg": "this planet does not exist, you can't update it"}), 200


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    query_results = User.query.filter_by(email=email).first()
    print(query_results)

    if query_results is None:
            return jsonify({"msg": "Bad Request"}), 404
    
    if email != query_results.email or password != query_results.password:
         return jsonify({"msg": "Bad email or password"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# @app.route("/signin", methods=["POST"])
# def signin():
#     email = request.json.get("email", None)
#     password = request.json.get("password", None)

#     query_results = User.query.filter_by(email=email).first()
#     print(query_results)

#     if query_results is None:
#             return jsonify({"msg": "Bad Request"}), 404
    
#     if email != query_results.email or password != query_results.password:
#          return jsonify({"msg": "Bad email or password"}), 401
    
#     access_token = create_access_token(identity=email)
#     return jsonify(access_token=access_token)

@app.route('/user', methods=['POST'])
def add_new_user():
    data = request.json
    name = request.json.get("name", None)

    user_exists = User.query.filter_by(name=data["name"]).first()
    
    if user_exists is None: 

            new_user = User(
                name=data["name"], 
                age=data["age"], 
                email=data["email"], 
                password=data["password"]
                )
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=name)
            return jsonify({
            "msg": "A new user has been added to the database",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"error": "User already exists"}), 400
           


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
