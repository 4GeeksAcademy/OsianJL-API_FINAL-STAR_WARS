import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    characters_id = Column(Integer, ForeignKey('characters.id'))
    planets_id = Column(Integer, ForeignKey('planets.id'))
    starships_id = Column(Integer, ForeignKey('starships.id'))
   
    
    
    

    def to_dict(self):
        return {}

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(250), nullable=False)
    user_favorites = relationship(Favorites)

    def to_dict(self):
        return {}

class Characters(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)
    mass = Column(Integer, nullable=False)
    hair_color = Column(String(250), nullable=False)
    eye_color = Column(String(250), nullable=False)
    gender = Column(String(250), nullable=False)
    birth_year = Column(String(250), nullable=False)
    characters_favorites = relationship(Favorites)
    

    def to_dict(self):
        return {}


class Planets(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    climate = Column(String(250), nullable=False)
    population = Column(Integer, nullable=False)
    orbital_period = Column(Integer, nullable=False)
    rotation_period = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    planets_favorites = relationship(Favorites)
    

    def to_dict(self):
        return {}
    
class Starships(Base):
    __tablename__ = 'starships'
    id = Column(Integer, primary_key=True)
    model = Column(String(250), nullable=False)
    manufacturer = Column(String(250), nullable=False)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    consumables = Column(String(250), nullable=False)
    cost_in_credits = Column(Integer, nullable=False)
    starships_favorites = relationship(Favorites)
    

    def to_dict(self):
        return {}
    


## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')


#   person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)