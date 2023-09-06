"""
File: main.py
Author: [Ranveer Dhaliwal]
Date: [2023-09-05]

Description:
This script connects to a Box Office web application
"""

# Imports from the 'website' directory 
from website import create_app  
from website.models import Movies

# Create a Flask web application instance using the 'create_app' function
app = create_app()

# Enter the application context to interact with the database
with app.app_context():

    #Retrieve the count of movies from the 'Movies' database, to ensure database is connected
    number_of_movies = Movies.query.count()
    print(f"Number of movies: {number_of_movies}")

if __name__ == '__main__':
    app.run(debug=True)