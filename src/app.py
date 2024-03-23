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

@app.route('/user', methods=['GET'])
def get_all_users():
    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(), query_results))

    if results == []:
        return jsonify("por el momento no hay usuarios"), 404
    
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
        return jsonify("por el momento no hay planetas"), 404
    
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
        return jsonify("por el momento no hay planetas"), 404
    
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
        return jsonify("por el momento no hay planetas"), 404
    
    response_body = {
        "msg": "ok",
        "results": results
    }
    
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    query_results = User.query.filter_by(id=user_id).first()
   

    if query_results is None:
        return jsonify({"msg": "ese usuario no existe"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    query_results = Planets.query.filter_by(id=planets_id).first()
   

    if query_results is None:
        return jsonify({"msg": "ese planeta no existe"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):
    query_results = Characters.query.filter_by(id=characters_id).first()
   

    if query_results is None:
        return jsonify({"msg": "ese personaje no existe"}), 404
    
    response_body = {
        "msg": "ok",
        "results": query_results.serialize()
    }
    return jsonify(response_body), 200

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_all_favorites_of_user(user_id):
    query_results = Favorites.query.filter_by(user_id=user_id).all()
    print(query_results)

    if query_results:
        results = list(map(lambda item: item.serialize(), query_results))
        return jsonify({"msg": "ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "there are not favorites"}), 404




@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
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
            return ({"msg": "it already has a favorite"}), 200
        
    elif user_exists is None and planets_exists is None:
        return ({"msg": "both user and planet do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif planets_exists is None: 
        return ({"msg": "this planet does not exist"}), 400
    
    
@app.route('/favorite/character/<int:characters_id>', methods=['POST'])
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
            return ({"msg": "it already has a favorite"}), 200
        
    elif user_exists is None and characters_exists is None:
        return ({"msg": "both user and character do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif characters_exists is None: 
        return ({"msg": "this character does not exist"}), 400    

 





@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
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

       

        
@app.route('/favorite/character/<int:user_id>/<int:characters_id>', methods=['DELETE'])
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

       



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
