#!/usr/bin/python3
"""

"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def return_state_list():
    states = storage.all(State)
    state_list = []
    for key, value in states.items():
        state_list.append(value.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def return_state_obj(state_id):
    states = storage.all(State)
    for key, value in states.items():
        if states[key].id == state_id:
            return value.to_dict()
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    state_json = request.get_json()
    if state_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in state_json:
        return (jsonify({'error': 'Not a JSON'}), 400)

    created_state = State(**state_json)
    created_state.save()
    return jsonify(created_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state_json = request.get_json()
    if state_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
