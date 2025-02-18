#!/usr/bin/python3
"""

"""

from models.place import Place
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def return_place_list(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def return_place_obj(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
    return(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    place_json = request.get_json()
    if city is None:
        abort(404)
    if place_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in place_json:
        return (jsonify({'error': 'Missing name'}), 400)
    if 'user_id' not in place_json:
                return (jsonify({'error': 'Missing user_id'}), 400)

    created_place =Place(**place_json)
    created_place.city_id = city_id
    created_place.save()
    return jsonify(created_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place_json = request.get_json()
    if place_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
