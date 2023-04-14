#!/usr/bin/python3
"""
Module contains the routes to be used for the API.
"""


from api.v1.views import app_views
import json
from flask import jsonify
from models import storage
from models.base_model import Base
from models.state import State
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status')
def app_status():
    """Returns the status code."""
    return jsonify({'status': 'OK'})
