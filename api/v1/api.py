#!/usr/bin/python3
import os
from flask import Flask
from api.v1.views import app_views
from app.models import storage


def create_api():
    api = Flask(__name__)

    # api.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    api.url_map.strict_slashes = False
    api.register_blueprint(app_views)

    return api


if __name__ == '__main__':
    api = create_api()
    # app.run(host='0.0.0.0', port=5001)
    api.run()
