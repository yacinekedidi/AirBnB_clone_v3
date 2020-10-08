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
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_of_city(city_id):
    """
    file: ./swag/places_all.yml
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_get(place_id):
    """
    file: ./swag/places_get.yml
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_del(place_id):
    """
    file: ./swag/places_del.yml
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_post(city_id=None):
    """
    file: ./swag/places_post.yml
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    if 'user_id' not in http_dict.keys():
        abort(400, description='Missing user_id')
    if not storage.get(User, http_dict['user_id']):
        abort(404)
    if 'name' not in http_dict.keys():
        abort(400, description='Missing name')
    place = Place(**http_dict)
    setattr(place, "city_id", city_id)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """
    file: ./swag/places_put.yml
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    for key, value in http_dict.items():
        if key not in ["id", "user_id", "city_id", "created_at",
                       "updated_at", "state_id"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def place_search_post():
    """
    file: ./swag/places_search.yml
    """
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    states = http_dict.get("states")
    cities = http_dict.get("cities")
    if not cities:
        cities = []
    amenities = http_dict.get("amenities")
    x = 0
    for k, v in http_dict.items():
        if len(v) > 0 and k in ["states", "cities", "amenities"]:
            x = 1

    if not len(http_dict) or x == 0:
        obj_list = []
        for key, obj in storage.all("Place").items():
            obj_list.append(obj.to_dict())
        return jsonify(obj_list)
    if states and len(states) > 0:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city.id not in cities:
                        cities.append(city.id)
    places = []
    if len(cities) > 0:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    places.append(place.to_dict())

    all_amenities = []
    if amenities and len(amenities) > 0:
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                all_amenities.append(amenity)
        places_obj = storage.all("Place").values()
        for place in places_obj:
            i = 0
            for amenity in all_amenities:
                if amenity not in place.amenities:
                    i = 1
                    break
            if i == 0:
                p = place.to_dict().copy()
                if "amenities" in p:
                    del p["amenities"]
                places.append(p)
    return jsonify(places)
