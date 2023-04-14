#!/usr/bin/python3
"""
This module is basis for the Flask API.
It contains the teardown and run configuration.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from models import storage
import threading
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*":{"origins":"0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(self):
    storage.close()

@app.errorhandler(404)
def page_not_found(err):
    status = {'error': 'Not found'}
    return jsonify(status), 404

if __name__ == "__main__":
    app_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    app_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=app_host, port=app_port, threaded=True)