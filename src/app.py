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

                                         ########DEFINIMOS NUESTROS ENDPOINTS############
#########################################################################################################################################


#########ENDPOINTS GET PARA OBTENER TODOS LOS REGISTROS DE UNA TABLA CONCRETA: 

#OBTENER TODOS LOS USUARIOS: 
@app.route('/all_users', methods=['GET'])
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

#OBTENER TODOS LOS PLANETAS
@app.route('/all_planets', methods=['GET'])
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

#OBTENER TODOS LOS PERSONAJES:
@app.route('/all_characters', methods=['GET'])
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

#OBTENER TODAS LAS NAVES ESPACIALES: 
@app.route('/all_starships', methods=['GET'])
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

#########ENDPOINTS GET PARA OBTENER UN REGISTRO CONCRETO DENTRO DE UNA TABLA:


#OBTENER UN USUARIO CONCRETO USANDO SU ID CON URL DINAMICA
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

#OBTENER UNA NAVE ESPACIAL CONCRETA USANDO SU ID CON URL DINAMICA
@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_one_starship(starship_id):
    query_result = Starships.query.filter_by(id=starship_id).first()

    if query_result is None:
         return jsonify({"msg": "there is no starship matching the Name provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result.serialize()
    }
    return jsonify(response_body), 200

#OBTENER UN PLANETA CONCRETO USANDO SU NOMBRE CON URL DINAMICA (cambiamos int por string)
@app.route('/planets/<string:planet_name>', methods=['GET'])
def get_one_planet(planet_name):
    query_result = Planets.query.filter_by(name=planet_name).first()
   

    if query_result is None:
        return jsonify({"msg": "there is no planet matching the Name provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result.serialize()
    }
    return jsonify(response_body), 200



#OBTENER UN PERSONAJE CONCRETO USANDO PARAMETROS DE CONSULTA EN LA URL (/characters?name=nombre_del_personaje)
@app.route('/characters', methods=['GET'])
def get_one_character():
    character_name = request.args.get("name")
    query_result = Characters.query.filter_by(name=character_name).first()
   

    if query_result is None:
        return jsonify({"msg": "there is no character matching the name provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result.serialize()
    }
    return jsonify(response_body), 200


####### OBTENER TODOS LOS FAVORITOS DE UN USUARIO ######
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_all_favorites_of_user(user_id):
    query_results = Favorites.query.filter_by(user_id=user_id).all()
    

    if query_results:
        results = list(map(lambda item: item.serialize(), query_results))
        return jsonify({"msg": "ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "this user has no favorites yet"}), 404


#########ENDPOINTS POST PARA CREAR REGISTROS EN LAS TABLAS: 
    
#CREAR UN USUARIO

@app.route('/user', methods=['POST'])
def add_new_user():
    data = request.json

    user_exists = User.query.filter_by(name=data["name"]).first()
    
    if user_exists is None: 

            new_user = User(
                name=data["name"], 
                email=data["email"], 
                password=data["password"]
                )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
            "msg": "A new user has been added to the database",
        }), 200
    else:
        return jsonify({"error": "User already exists"}), 400
    

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
                # orbital_period=data["orbital_period"], 
                # rotation_period=data["rotation_period"], 
                # diameter=data["diameter"]
                )
            db.session.add(new_planet)
            db.session.commit()
            return ({"msg": "ok, a new planet has been added to the database"}), 200

       

    else:
            return ({"msg": "this planet is already included in the database"}), 200
    

#CREAR UNA NAVE ESPACIAL NUEVA
@app.route('/starship', methods=['POST'])
def add_new_starship():
    data = request.json
    print(data)

    starship_exists = Starships.query.filter_by(model=data["model"]).first()
    
    if starship_exists is None: 

            new_starship = Starships(
                model=data["model"], 
                manufacturer=data["manufacturer"], 
                crew=data["crew"], 
                # orbital_period=data["orbital_period"], 
                # rotation_period=data["rotation_period"], 
                # diameter=data["diameter"]
                )
            db.session.add(new_starship)
            db.session.commit()
            return ({"msg": "ok, a new starship has been added to the database"}), 200

       

    else:
            return ({"msg": "this starship is already included in the database"}), 200
    

#CREAR UN PERSONAJE NUEVO
@app.route('/character', methods=['POST'])
def add_new_character():
    data = request.json
    print(data)

    character_exists = Characters.query.filter_by(name=data["name"]).first()
    
    if character_exists is None: 

            new_character = Characters(
                name=data["name"], 
                height=data["height"], 
                mass=data["mass"], 
                # orbital_period=data["orbital_period"], 
                # rotation_period=data["rotation_period"], 
                # diameter=data["diameter"]
                )
            db.session.add(new_character)
            db.session.commit()
            return ({"msg": "ok, a new character has been added to the database"}), 200

       

    else:
            return ({"msg": "this character is already included in the database"}), 200

################# AÑADIR FAVORITOS PARA USUARIOS ################################

# AÑADIR PLANETA FAVORITO USANDO IDs EN LA URL DINAMICA 
@app.route('/favorites/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_new_favorite_planet(planet_id,user_id):

    user_exists = User.query.filter_by(id=user_id).first()
    planets_exists = Planets.query.filter_by(id=planet_id).first()
    
    if user_exists and planets_exists: 


        query_results = Favorites.query.filter_by(planets_id=planet_id, user_id=user_id).first()

        if query_results is None: 

            new_favorite = Favorites(planets_id=planet_id, user_id=user_id)
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
    

# AÑADIR NAVE ESPACIAL FAVORITA USANDO IDs EN LA URL DINAMICA 
@app.route('/favorites/starship/<int:starship_id>/<int:user_id>', methods=['POST'])
def add_new_favorite_starship(starship_id,user_id):

    user_exists = User.query.filter_by(id=user_id).first()
    starships_exists = Starships.query.filter_by(id=starship_id).first()
    
    if user_exists and starships_exists: 


        query_results = Favorites.query.filter_by(starships_id=starship_id, user_id=user_id).first()

        if query_results is None: 

            new_favorite = Favorites(starships_id=starship_id, user_id=user_id)
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200

       

        else:
            return ({"msg": "this user already has this starship as a favorite"}), 200
        
    elif user_exists is None and starships_exists is None:
        return ({"msg": "both user and starship do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif starships_exists is None: 
        return ({"msg": "this starship does not exist"}), 400
    
#AÑADIR PERSONAJE FAVORITO (usando request.json: el cliente nos tiene que enviar ambos IDs en el body)
@app.route('/favorites/character', methods=['POST'])
def add_new_favorite_character():
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


############################### ACTUALIZAR REGISTROS EN LA BASE DE DATOS USANDO PUT#########################
    
#ACTUALIZAR USUARIO (USANDO SU NOMBRE COMO COINCIDENCIA DENTRO DEL BODY)    
@app.route('/user', methods=['PUT'])
def update_user():
    data = request.json

    user = User.query.filter_by(name=data["name"]).first()
    
    if user: 
    
            user.name=data["name"], 
            user.email=data["email"],
            user.password=data["password"]
                
            
            db.session.commit()
            return ({"msg": "ok, the user has been updated in the database"}), 200

       

    else:
            return ({"msg": "this user does not exist, you can't update it"}), 200


 
# ACTUALIZAR DATOS DE UN PLANETA USANDO URL DINAMICA E ID DEL PLANETA
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    data = request.json

    planet = Planets.query.filter_by(id=planet_id).first()
    
    if planet: 
    
            planet.name=data["name"], 
            planet.climate=data["climate"], 
            planet.population=data["population"], 
            # planet.orbital_period=data["orbital_period"], 
            # planet.rotation_period=data["rotation_period"], 
            # planet.diameter=data["diameter"]
                
            
            db.session.commit()
            return ({"msg": "ok, the planet has been updated in the database"}), 200

       

    else:
            return ({"msg": "this planet does not exist, you can't update it"}), 200

############################### BORRAR REGISTROS EN LA BASE DE DATOS USANDO DELETE#########################

# BORRAR USUARIO EN BASE A SU NOMBRE        
@app.route('/user', methods=['DELETE'])
def delete_user():
    data = request.json

    user_exists = User.query.filter_by(name=data["name"]).first()
    
    if user_exists: 
         
            db.session.delete(user_exists)
            db.session.commit()
            return ({"msg": "ok, its deleted"}), 200

        

    else: 

           return ({"msg": "there is nothing to delete"}), 200
    

# BORRAR TODOS LOS USUARIOS       
@app.route('/users', methods=['DELETE'])
def delete_all_users():
    users_deleted = User.query.delete()
    db.session.commit()
    
    if users_deleted > 0: 
            return ({"msg": "ok, all users have been deleted"}), 200

    else: 

           return ({"msg": "there are no users to delete"}), 200
    

########## BORRAR UN PLANETA FAVORITO DE UNA CUENTA DE UN USUARIO#############################
    
# 1 #PRIMER MÉTODO, USANDO EL REQUEST.JSON PARA SABER IDS DE USUARIO Y PLANETA
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

       

# 2 # SEGUNDO MÉTODO, USANDO LA URL DINÁMICA PARA SABER IDS DE USUARIO Y PLANETA (METODO OPTIMO)        
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
    






##################GENERAR UN TOKEN AL HACER UN LOGIN#######################
    
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

# Protect a route with jwt_required, which will kick out requests without a valid JWT
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    email = get_jwt_identity()
    print(email)
    user = User.query.filter_by(email=email).first()
    
    return jsonify({"got it": user.name }), 200

           


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
