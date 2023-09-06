"""
File: models.py
Author: [Ranveer Dhaliwal]
Date: [2023-09-05]

Description:
Sefines the database models for a Flask web application that manages movies.
It includes the 'User' and 'Movies' classes that represent tables in the database.
"""
# Import necessary modules and classes
from . import db                     #importing the db from __INIT__
from flask_login import UserMixin    # Import the 'UserMixin' class for user model
from sqlalchemy.sql import func      # Import 'func' for database function    



class User(db.Model, UserMixin):

    """
    Class: User(db.Model, UserMixin)

    Represents the 'user' table in the database.

    Attributes:
    - id : Unique identifier for each user. This is the Primary Key
    - email: User's email address (max 150 characters, unique).
    - password: User's password (max 150 characters).
    - firstName: User's first name (max 150 characters).

    """
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
  


class Movies( db.Model):
    """
    Class: Movies(db.Model)

    Represents the 'movies' table in the database.

    Attributes:
    - id: Unique identifier for each movie. This is the Primary Key
    - title: Movie title (max 255 characters, not nullable).
    - genre: Movie genre (max 150 characters).
    - publish_year: Year the movie was published.
    - description: Movie description (max 2000 characters).
    - user_rating: User rating for the movie (default is None).
    """
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(150))
    publish_year = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    user_rating = db.Column(db.Integer, default=None)
    
    

