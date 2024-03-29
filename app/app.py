#!/usr/bin/python3
import os
from flask import Flask
from app.models import storage
from app.routes import register_routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'eventibuzz.sqlite'),
    )

    # Configurations
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Set strict_slashes=False for all routes
    app.url_map.strict_slashes = False

    register_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    # app.run(host='0.0.0.0', port=5000)
    # initialize_database(app)
    app.run()
