"""
File: __init__.py
Author: [Ranveer Dhaliwal]
Date: [2023-09-05]

Description:
This module initializes Box Office application, configures the database, and registers blueprints.
It also sets up user authentication using Flask-Login and defines functions for database creation
and populating movie data.

"""
# Import necessary modules and classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy and database
db = SQLAlchemy()
DB_NAME = "database.db"


# Function to create and configure the Flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'talon'             #Encrypt session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import views and auth blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import databases from models
    from .models import User, Movies

    # Configure and initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    @login_manager.user_loader    
    def load_user(id):
        return User.query.get(int(id))

    # Create the database and populate movie dat
    create_database(app)
    populate_movies_database(app)
    
    return app

# Function to create the database if it doesn't exist
def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
            db.create_all(app=app)
            print("DB Created")


# Function to populate the 'Movies' table with data if it's empty
def populate_movies_database(app):

    from .models import Movies
    with app.app_context():
        if Movies.query.count() == 0:
            movies_data = [
                    {"title": "The Shawshank Redemption", "genre": "Drama", "publish_year": 1994, "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
                    {"title": "Pulp Fiction", "genre": "Crime/Drama", "publish_year": 1994, "description": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in a series of interconnected stories."},
                    {"title": "The Matrix", "genre": "Action/Sci-Fi", "publish_year": 1999, "description": "A computer programmer discovers a dystopian world controlled by machines and joins a group of rebels fighting against them."},
                    {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Adventure/Fantasy", "publish_year": 2001, "description": "A young hobbit and a group of companions set out on a journey to destroy a powerful ring and save their world from darkness."},
                    {"title": "Avatar", "genre": "Action/Adventure", "publish_year": 2009, "description": "A paraplegic marine is sent to the moon Pandora, where he becomes torn between following orders and protecting the alien civilization."},
                    {"title": "Inception", "genre": "Action/Sci-Fi", "publish_year": 2010, "description": "A thief who enters people's dreams to steal their secrets is offered a chance to regain his old life as payment for a seemingly impossible task."},
                    {"title": "The Dark Knight", "genre": "Action/Crime", "publish_year": 2008, "description": "Batman faces off against the Joker, a mastermind criminal wreaking havoc on Gotham City."},
                    {"title": "Toy Story", "genre": "Animation/Adventure", "publish_year": 1995, "description": "A cowboy doll and a space action figure form an unlikely friendship and go on a journey to return to their owner."},
                    {"title": "Titanic", "genre": "Drama/Romance", "publish_year": 1997, "description": "A young aristocrat falls in love with a kind but poor artist aboard the ill-fated R.M.S. Titanic."},
                    {"title": "Gladiator", "genre": "Action/Drama", "publish_year": 2000, "description": "A former Roman general seeks vengeance against the corrupt emperor who murdered his family and condemned him to slavery."},
                    {"title": "The Avengers", "genre": "Action/Sci-Fi", "publish_year": 2012, "description": "Earth's mightiest heroes come together to stop an alien invasion led by the villainous Loki."},
                    {"title": "Harry Potter and the Sorcerer's Stone", "genre": "Adventure/Fantasy", "publish_year": 2001, "description": "A young boy discovers he's a wizard and enrolls in a magical school, where he uncovers his destiny."},
                    {"title": "The Lion King", "genre": "Animation/Adventure", "publish_year": 1994, "description": "A young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery."},
                    {"title": "Forrest Gump", "genre": "Drama/Romance", "publish_year": 1994, "description": "A man with a low IQ experiences several historical events and unwittingly influences them."},
                    {"title": "Frozen", "genre": "Animation/Adventure", "publish_year": 2013, "description": "Two sisters in a kingdom trapped in eternal winter must save their realm with the help of magical allies."},
                    {"title": "The Social Network", "genre": "Biography/Drama", "publish_year": 2010, "description": "The story of the creation of Facebook and the legal battles that followed among its founders."},
                    {"title": "The Revenant", "genre": "Adventure/Drama", "publish_year": 2015, "description": "A frontiersman on a fur trading expedition fights for survival after being mauled by a bear and left for dead."},
                    {"title": "Black Panther", "genre": "Action/Sci-Fi", "publish_year": 2018, "description": "T'Challa, the king of Wakanda and the Black Panther, must defend his kingdom against threats from within and outside."},
                    {"title": "The Grand Budapest Hotel", "genre": "Adventure/Comedy", "publish_year": 2014, "description": "The adventures of a legendary hotel concierge and his lobby boy amidst the backdrop of a changing Europe."},
                    {"title": "La La Land", "genre": "Drama/Musical", "publish_year": 2016, "description": "A jazz musician and an aspiring actress fall in love in Los Angeles while pursuing their dreams."}
                ]
            
            for movie_info in movies_data:
                movie = Movies( 
                    title=movie_info['title'],
                    genre=movie_info['genre'],
                    publish_year=movie_info['publish_year'],
                    description=movie_info['description'],
                    user_rating= None
                )
                db.session.add(movie)
            db.session.commit()
            print("Populated Movies Data!")





