from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#DEFINIMOS NUESTRAS TABLAS Y LAS RELACIONES ENTRE ELLAS, AÑADIENDO LOS ATRIBUTOS CORRESPONDIENTES:

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    starships_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
   


    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
            "starships_id": self.starships_id
        }
    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=True)
    user_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    characters_favorites = db.relationship(Favorites)

    
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.height,
            "hair_color": self.height,
            "eye_color": self.height,
            "gender": self.height,
            "birth_year": self.height,
            
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    planets_favorites = db.relationship(Favorites)

    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
           
        }
    
class Starships(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    starships_favorites = db.relationship(Favorites)

    
    def __repr__(self):
        return '<Starships %r>' % self.model

    def serialize(self):
        return {
            "id": self.id,
            "manufacturer": self.manufacturer,
            "crew": self.crew,
            "passengers": self.passengers,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "model": self.model
        
        }
    




