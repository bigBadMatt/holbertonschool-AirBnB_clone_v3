#!/usr/bin/python3
"""

"""

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def return_city_list(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return (jsonify({'error': 'State isnt'}), 400)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def return_city_obj(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
    return(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    city_json = request.get_json()
    if state is None:
        abort(404)
    if city_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in city_json:
        return (jsonify({'error': 'Not a JSON'}), 400)

    created_city = City(**city_json)
    created_city.state_id = state_id
    created_city.save()
    return jsonify(created_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city_json = request.get_json()
    if city_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    for key, value in city_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
