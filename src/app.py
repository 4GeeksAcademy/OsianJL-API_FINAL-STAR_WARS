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
    result_id = [item.id for item in query_results]
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

#OBTENER UN PLANETA CONCRETO USANDO URL DINAMICA (cambiamos int por string)
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    query_result = Planets.query.filter_by(id=planet_id).first()
   

    if query_result is None:
        return jsonify({"msg": "there is no planet matching the Name provided"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_result.serialize()
    }
    return jsonify(response_body), 200



#OBTENER UN PERSONAJE CONCRETO USANDO URL DINAMICA
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_character(character_id):

    query_result = Characters.query.filter_by(id=character_id).first()
    print(query_result)
    if query_result is None:
        return jsonify({"msg": "there is no character matching the name provided"}), 404
    
    response_body = {
        "msg": "ok",
        "id": query_result.id,
        "results": query_result.serialize()
    }
    return jsonify(response_body), 200


####### OBTENER TODOS LOS FAVORITOS DE UN USUARIO ######
@app.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_all_favorites_of_user():
    email = get_jwt_identity()

    user_exists = User.query.filter_by(email=email).first()

    if user_exists is None: 
           return jsonify({"msg": "This user does not exist"}), 401

    user_id = user_exists.id

    query_results = Favorites.query.filter_by(user_id=user_id).all()

    # planet_exists = Planets.query.filter_by(id=planet_id).first()
    

    if query_results:
        results = list(map(lambda item: item.serialize(), query_results))
        print(results)
        return jsonify({"msg": "ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "this user has no favorites yet"}), 404

# @jwt_required()
# def add_new_favorite_planet(planet_id):

#     email = get_jwt_identity()
  

#     user_exists = User.query.filter_by(email=email).first()

#     if user_exists is None: 
#            return jsonify({"msg": "This fucking user does not exist"}), 401

#     user_id = user_exists.id

#     planet_exists = Planets.query.filter_by(id=planet_id).first()
    
#     if planet_exists is None: 
#            return jsonify({"msg": "This fucking planet does not exist"}), 401
    
    
#     query_results = Favorites.query.filter_by(planets_id=planet_id, user_id=user_id).first()
#     print(query_results)
#     if query_results is None: 

#             new_favorite = Favorites(planets_id=planet_id, user_id=user_id)
#             new_planet = Planets.query.filter_by(id=planet_id).first()
#             db.session.add(new_favorite)
#             db.session.commit()

#             response_body = {
#                  "msg": "ok", 
#                  "results": new_planet.serialize()
#             }
#             return jsonify(response_body), 200 

#########ENDPOINTS POST PARA CREAR REGISTROS EN LAS TABLAS: 
    
#CREAR UN USUARIO

@app.route('/user', methods=['POST'])
def add_new_user():
    data = request.json

    user_exists = User.query.filter_by(first_name=data["first_name"]).first()
    
    if user_exists is None: 

            new_user = User(
                first_name=data["first_name"], 
                last_name=data["last_name"], 
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
                orbital_period=data["orbital_period"], 
                rotation_period=data["rotation_period"], 
                diameter=data["diameter"]
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
                passengers=data["passengers"], 
                consumables=data["consumables"], 
                cost_in_credits=data["cost_in_credits"]
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
                hair_color=data["hair_color"], 
                eye_color=data["eye_color"], 
                gender=data["gender"],
                birth_year=data["birth_year"]
                )
            db.session.add(new_character)
            db.session.commit()
            return ({"msg": "ok, a new character has been added to the database"}), 200

       

    else:
            return ({"msg": "this character is already included in the database"}), 200

################# AÑADIR FAVORITOS PARA USUARIOS ################################

# AÑADIR PLANETA FAVORITO USANDO IDs EN LA URL DINAMICA 
# @app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
# @jwt_required()
# def add_new_favorite_planet(planet_id):

#     email = get_jwt_identity()
  

#     user_exists = User.query.filter_by(email=email).first()

#     if user_exists is None: 
#            return jsonify({"msg": "This user does not exist"}), 401

#     user_id = user_exists.id

#     planet_exists = Planets.query.filter_by(id=planet_id).first()
    
#     if planet_exists is None: 
#            return jsonify({"msg": "This fucking planet does not exist"}), 401
    
    
#     query_results = Favorites.query.filter_by(planets_id=planet_id, user_id=user_id).first()
#     print(query_results)
#     if query_results is None: 

#             new_favorite = Favorites(planets_id=planet_id, user_id=user_id)
#             new_planet = Planets.query.filter_by(id=planet_id).first()
#             db.session.add(new_favorite)
#             db.session.commit()

#             response_body = {
#                  "msg": "ok", 
#                  "results": new_planet.serialize()
#             }
#             return jsonify(response_body), 200 

#     else:
#             return ({"msg": "this user already has this planet as a favorite"}), 200
        
  
    
@app.route('/favorites/<int:item_id>', methods=['POST'])
@jwt_required()
def add_new_favorite(item_id):
    data = request.json()
    email = get_jwt_identity()
    item_type = data.item_type

    user_exists = User.query.filter_by(email=email).first()

    if user_exists is None: 
           return jsonify({"msg": "This user does not exist"}), 401

    user_id = user_exists.id

   
    if item_type is "planet":

        planet = Planets.query.filter_by(id=item_id).first()
        if planet is None: 
           return jsonify({"msg": "This planet does not exist"}), 401
        new_favorite = Favorites(planets_id=item_id, user_id=user_id)
        db.session.add(new_favorite)
        db.session.commit()
        response_body = {
                 "msg": "ok", 
                 "results": planet.serialize()
            }
        return jsonify(response_body), 200 

    if item_type is "character":
        character = Characters.query.filter_by(id=item_id).first()
        if character is None: 
           return jsonify({"msg": "This character does not exist"}), 401
        new_favorite = Favorites(characters_id=item_id, user_id=user_id)
        db.session.add(new_favorite)
        db.session.commit()
        response_body = {
                 "msg": "ok", 
                 "results": character.serialize()
            }
        return jsonify(response_body), 200 

    if item_type is "starship":
        starship = Starships.query.filter_by(id=item_id).first()
        if starship is None: 
           return jsonify({"msg": "This starship does not exist"}), 401
        new_favorite = Favorites(starships_id=item_id, user_id=user_id)
        db.session.add(new_favorite)
        db.session.commit()
        response_body = {
                 "msg": "ok", 
                 "results": starship.serialize()
            }
        return jsonify(response_body), 200 


    # else:
    #         return ({"msg": "this user already has this planet as a favorite"}), 200
    

# AÑADIR NAVE ESPACIAL FAVORITA USANDO IDs EN LA URL DINAMICA 
@app.route('/favorites/starship/<int:starship_id>', methods=['POST'])
@jwt_required()
def add_new_favorite_starship(starship_id):

    email = get_jwt_identity()

    user_exists = User.query.filter_by(email=email).first()

    if user_exists is None: 
           return jsonify({"msg": "This user does not exist"}), 401

    user_id = user_exists.id

    starships_exists = Starships.query.filter_by(id=starship_id).first()

    if starships_exists is None: 
           return jsonify({"msg": "This starship does not exist"}), 401
    

    query_results = Favorites.query.filter_by(starships_id=starship_id, user_id=user_id).first()

    if query_results is None: 

            new_favorite = Favorites(starships_id=starship_id, user_id=user_id)
            new_starship = Starships.query.filter_by(id=starship_id).first()
            db.session.add(new_favorite)
            db.session.commit()

            response_body = {
                 "msg": "ok", 
                 "results": new_starship.serialize()
            }
            return jsonify(response_body), 200 

    else:
            return ({"msg": "this user already has this starship as a favorite"}), 200
    
#AÑADIR PERSONAJE FAVORITO (usando request.json: el cliente nos tiene que enviar ambos IDs en el body)
@app.route('/favorites/character/<int:character_id>', methods=['POST'])
@jwt_required()
def add_new_favorite_character(character_id):
    email = get_jwt_identity()
    
    user_exists = User.query.filter_by(email=email).first()

    if user_exists is None:
         return jsonify({"msg": "this user does not exist"}), 401
    
    user_id = user_exists.id

    characters_exists = Characters.query.filter_by(id=character_id).first()
    
    if characters_exists is None:
         return jsonify({"msg": "this character does not exist"}), 401
   
    query_results = Favorites.query.filter_by(characters_id=character_id, user_id=user_id).first()

    if query_results is None: 

            new_favorite = Favorites(characters_id=character_id, user_id=user_id)
            new_character = Characters.query.filter_by(id=character_id).first()
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok", "results": new_character.serialize()}), 200

    else:
            return ({"msg": "this user already has this character as a favorite"}), 200
        


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

       
#BORRAR UN FAVORITO USANDO EL ID DEL FAVORITO @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(favorite_id):
    email = get_jwt_identity()

    user_exists = User.query.filter_by(email=email).first()
    if user_exists is None: 
            return jsonify({"msg": "this user does not exist"})
    
    user_id = user_exists.id

    favorite_exists = Favorites.query.filter_by(id=favorite_id).first()
    if favorite_exists is None: 
            return jsonify({"msg": "this favorite does not exist"})
    

    query_results = Favorites.query.filter_by(id=favorite_id, user_id=user_id).first()

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

# # BORRAR TODOS LOS PLANETAS        
# @app.route('/planets', methods=['DELETE'])
# def delete_all_planets():
   
#     planets_deleted = Planets.query.delete()
#     db.session.commit()
    
#     if planets_deleted > 0: 
#             return ({"msg": "ok, all planets have been deleted"}), 200

#     else: 

#            return ({"msg": "there are no planets to delete"}), 200
    






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


#SIGN IN ############################################################################################
@app.route("/signin", methods=["POST"])
def signin():
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user_exists = User.query.filter_by(email=email).first()
    
    if user_exists is None: 

            new_user = User(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                password=password
                )
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
            
    else:
        return jsonify({"error": "User already exists"}), 400

    
   



# PROTEGER UNA RUTA
@app.route("/favorites", methods=["GET"])
@jwt_required()
def favorites_protected():
    # Access the identity of the current user with get_jwt_identity
    email = get_jwt_identity()
    print(email)

    user = User.query.filter_by(email=email).first()
    print(user)
    
    if user is None: 
           return jsonify("wrong authorization/restricted area"), 401

    
    user_favorites = Favorites.query.filter_by(user_id=user.id).all()

    if user_favorites:
    
        results = list(map(lambda item: item.serialize(), user_favorites))
        return jsonify({"msg": "ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "this user has no favorites yet"}), 404


# CONDICIONAL RENDERING #############################################################################

@app.route("/valid-token", methods=["GET"])
@jwt_required()
def valid_token():
     current_user = get_jwt_identity()
     querty_results = User.query.filter_by(email=current_user).first()
     if querty_results is None:
            return jsonify({"msg": "user does not exist",
                           "is_logged": False}), 404
     
     return jsonify({"is_logged": True}), 200
          





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
