#!/usr/bin/python3
"""

"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def return_amenity_list():
    amenities = storage.all(Amenity)
    amenity_list = []
    for key, value in amenities.items():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def return_amenity_obj(amenity_id):
    amenities = storage.all(Amenity)
    for key, value in amenities.items():
        if amenities[key].id == amenity_id:
            return value.to_dict()
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    amenity_json = request.get_json()
    if amenity_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in amenity_json:
        return (jsonify({'error': 'Not a JSON'}), 400)

    created_amenity = Amenity(**amenity_json)
    created_amenity.save()
    return jsonify(created_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    amenity_json = request.get_json()
    if amenity_json is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
