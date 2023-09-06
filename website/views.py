
"""
File: views.py
Author: [Ranveer Dhaliwal]
Date: [2023-09-05]

Description:
This module defines routes and views for a Flask web application that manages a movie database.
It includes functions for rendering HTML templates, adding, deleting, login\sign-up and rating movies. 
It also protects routes with authentication using Flask-Login.

"""

# Import necessary modules and classes
from . import db
from flask import redirect, url_for
from flask import Blueprint, render_template, request, flash
from flask_login import  login_required,  current_user
from .models import Movies


# Create a Blueprint for views
views = Blueprint('views',__name__)



# Define route and view functions

#displays the home page of the application
@views.route('/', methods =['GET', 'POST'])
@login_required
def home():
    """
    Route: '/'
    View: home()

    Renders the home page of the web application.

    Args:
    - None

    Returns:
    - Rendered 'home.html' template with the 'current_user' object.

    """
    return render_template("home.html", user=current_user)


#displays all the movies in the database
@views.route('/movies', methods= ['GET'])       
@login_required         
def movies():
    """
    Route: '/movies'
    View: movies()

    Displays all the movies in the database.

    Args:
    - None

    Returns:
    - Rendered 'movies.html' template with the 'current_user' and 'movies_list' objects.

    """
    movies_list = Movies.query.all()
    return render_template("movies.html", user=current_user, movies=movies_list)


# review\update review a movie
@views.route('/movieRating/<int:movie_id>', methods = ['GET', 'POST'])  
@login_required
def rating(movie_id):
    """
    Route: '/movieRating/<int:movie_id>'
    View: rating(movie_id)

    Allows users to review and rate a movie.

    Args:
    - movie_id (int): The ID of the movie to review.

    Returns:
    - Rendered 'rating_page.html' template with the 'current_user' and 'movie' objects.

    """

    movie = Movies.query.get_or_404(movie_id) #finds the movie, if  not found, abort with 404 instead of 'none'
    
    if request.method == 'POST':
        rating = request.form.get('new_text')

        if int(rating) <0 or int(rating) >100:
            flash('Invalid rating, rating must be between 0-100', category='error')
        else:
            movie.user_rating = rating
            db.session.commit() 
            flash(f'You have rated {movie.title}', category='success') 
            return redirect(url_for('views.movies'))
    return render_template("rating_page.html", user = current_user, movie = movie)

#add a new movie to the database
@views.route('/add_movie', methods = ['GET', 'POST'])       
@login_required
def add_movie():
    """
    Route: '/add_movie'
    View: add_movie()

    Allows users to add a new movie to the database.

    Args:
    - None

    Returns:
    - If the request is POST, it adds the movie to the database and redirects to the movies page.
    - Otherwise, it renders the 'add_movie.html' template with the 'current_user' object.

    """
  
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        publish_year = request.form.get('publish_year')
        description = request.form.get('description')
        user_rating = request.form.get('user_rating')

        db_title = Movies.query.filter_by(title=title).first()

        if db_title:
            flash('Movie already exists', category='error')
        elif len(title) <= 0:
            flash('Title must be atleast 1 character', category='error')
        elif len(genre) <2:
            flash('Genre must be atleast 2 character', category='error')
        elif int(publish_year) <1900:
            flash('Year published must be from after 1900', category='error')
        elif len(description) > 2000:
            flash('Description must be less than 2000 characters', category='error')
        else:
            new_movie = Movies(title=title, genre=genre, publish_year=publish_year, description=description, user_rating=user_rating)
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie has been added!', category='success')
           
            return redirect(url_for('views.movies'))

    return render_template("add_movie.html", user = current_user)


#delete a movie from db
@views.route('/delete_movie/<int:movie_id>', methods = ['GET', 'POST'])  
@login_required
def delete_movie(movie_id):

    """
    Route: '/delete_movie/<int:movie_id>'
    View: delete_movie(movie_id)

    Allows users to delete a movie from the database.

    Args:
    - movie_id (int): The ID of the movie to delete.

    Returns:
    - Redirects to the movies page after deleting the movie.
    """
    
    movie = Movies.query.get_or_404(movie_id)
    movie_title = movie.title

    db.session.delete(movie)
    db.session.commit()

    flash(f'{movie_title} was removed', category='success')
    return redirect(url_for('views.movies'))











