#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenity_of_a_place(place_id):
    """
    file: amenity_by_place.yml
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_del(place_id, amenity_id):
    """
    file: amenity_by_place_delete.yml
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    else:
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_post(place_id, amenity_id):
    """
    file: amenity_post.yml
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
