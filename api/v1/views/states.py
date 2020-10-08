#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', methods=('GET',), strict_slashes=False)
@app_views.route('/states', methods=('GET',), strict_slashes=False)
def states_get(state_id=None):
    """
    file: ./swag/states_get.yml
    """
    if not state_id:
        obj_list = []
        for key, obj in storage.all("State").items():
            obj_list.append(obj.to_dict())
        return jsonify(obj_list)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        else:
            return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=('DELETE',),
                 strict_slashes=False)
def states_del(state_id=None):
    """
    file: ./swag/states_del.yml
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=('POST',), strict_slashes=False)
def states_post():
    """
    file: ./swag/states_post.yml
    """
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    if 'name' not in http_dict.keys():
        abort(400, description='Missing name')
    state = State(**http_dict)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=('PUT',), strict_slashes=False)
def states_put(state_id=None):
    """ Adds a new State instance """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    for key, value in http_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
