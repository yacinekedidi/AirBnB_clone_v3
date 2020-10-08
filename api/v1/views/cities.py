#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city_of_a_state(state_id):
    """
    file: ./swag/city_by_state.yml
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_get(city_id):
    """
    file: ./swag/city.yml
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_del(city_id):
    """
    file: ./swag/city_del.yml
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """
    file: ./swag/city_post.yml
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, 'Not a JSON')
    if 'name' not in http_dict.keys():
        abort(400, 'Missing name')
    http_dict["state_id"] = state_id
    city = City(**http_dict)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """
    file: ./swag/city_put.yml
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, 'Not a JSON')
    for key, value in http_dict.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
