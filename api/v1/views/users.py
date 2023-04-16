#!/usr/bin/python3
"""

"""

from models.user import User
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def return_user_list():
    users = storage.all(User)
    user_list = []
    for key, value in users.items():
        user_list.append(value.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def return_user_obj(user_id):
    users = storage.all(User)
    for key, value in users.items():
        if users[key].id == user_id:
            return value.to_dict()
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    user_json = request.get_json()
    if user_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in user_json:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in user_json:
        return (jsonify({'error': 'Missing password'}), 400)

    created_user = User(**user_json)
    created_user.save()
    return jsonify(created_user.to_dict()), 201

@app_views.route('/userss/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user_json = request.get_json()
    if user_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in user_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
