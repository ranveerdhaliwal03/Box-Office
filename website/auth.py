"""
File: auth.py
Author: [Ranveer Dhaliwal]
Date: [2023-09-05]

Description:
This module defines authentication routes and views for the Box Office web application.
It includes functions for user login, logout, and sign-up.

"""


# Import necessary modules and classes
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash  #allows for the passowords to be saved so its not in plain text
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication
auth = Blueprint('auth',__name__)

# Define authentication routes and view functions

#Login
@auth.route('/login', methods=["GET","POST"])
def login():
    """
    Route: '/login'
    View: login()

    Allows users to log in with their email and password.

    Args:
    - None

    Returns:
    - If the request is POST and login is successful, it redirects to the home page.
    - If login fails, it displays an error message.
    - If the request is GET, it renders the 'login.html' template.

    """
    if request.method =='POST':         #when user presses submit button, store the data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filter databbase to show the people with that email
        if user:
            if check_password_hash(user.password, password):
                flash('You are logged in!', category='success')
                login_user(user,remember= True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Please try again', category='error')
        else:
            flash('Email does not exist')


    return render_template("login.html",user=current_user) 


#Logout
@auth.route('/logout')
@login_required
def logout():

    """
    Route: '/logout'
    View: logout()

    Logs out the current user and redirects to the login page.

    Args:
    - None

    Returns:
    - Redirects to the login page.

    """
    logout_user()
    return redirect(url_for('auth.login')) 

#Sign-up
@auth.route('/sign-up', methods=["GET","POST"])
def sign_up():

    """
    Route: '/sign-up'
    View: sign_up()

    Allows users to create a new account with their email, first name, and password.

    Args:
    - None

    Returns:
    - If the request is POST and sign-up is successful, it logs in the user and redirects to the home page.
    - If sign-up fails, it displays an error message.
    - If the request is GET, it renders the 'sign_up.html' template.

    """

    if request.method =='POST':         #when user presses submit button, store the data
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist', category='error')
        elif len(email) <4:
            flash('Email must be greater than 4 characters', category="error")
        elif len(firstName) <2:
            flash('First name  must be greater than 1 character', category="error")
        elif password1 != password2:
            flash('password does not match', category="error")
        elif len(password1)<7:
            flash('password must be greater than 7 characters', category="error")
        else:
            new_user = User(email=email,firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category="success")  
            login_user(user,remember= True)     
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)   
