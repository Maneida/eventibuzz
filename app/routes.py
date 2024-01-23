#!/usr/bin/python3
import os
from flask import render_template, redirect, session, url_for, send_from_directory
from app.models import storage

def register_routes(app):
    """
    Register routes with the Flask application.

    Args:
        app (Flask): The Flask application.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def teardown_db(exception):
        """
        after each request, this method calls .close() (i.e. .remove()) on
        the current SQLAlchemy Session
        """
        storage.close()

    @app.route('/favicon.ico')
    def favicon():
        return url_for('static', filename='images/favicon.ico')

    # ********************************************************************

    # @app.route('/')
    @app.route('/home')
    @app.route('/index')
    def index():
        """renders index or home page"""
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        """renders login page"""
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/register')
    
    @app.route('/profile/<user_id>')
    def user_profile(user_id):
        """User profile page"""
        return render_template('user.html', user_id=user_id)

    @app.route('/about')

    @app.route('/contact')

    # ********************************************************************

    @app.route('/', strict_slashes=False)
    def welcome():
        """A route that returns a greeting message."""
        return '<p style="font-size: 54px;">Welcome!!!</p>'

    @app.route('/ping', strict_slashes=False)
    def pingpong():
        """A route that returns a ping-pong response."""
        return 'Pong!'


    @app.route('/x', strict_slashes=False)
    def first_render():
        return render_template('base.html')

    @app.route('/landing-page', strict_slashes=False)
    def landing_page():
        return render_template('landing-page.html')


