#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users/<user_id>',
                 methods=('GET',), strict_slashes=False)
@app_views.route('/users', methods=('GET',), strict_slashes=False)
def users_get(user_id=None):
    """
    file: ./swag/users_get.yml
    """
    if not user_id:
        obj_list = []
        for key, obj in storage.all("User").items():
            obj_list.append(obj.to_dict())
        return jsonify(obj_list)
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        else:
            return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=('DELETE',),
                 strict_slashes=False)
def users_del(user_id=None):
    """
    file: ./swag/users_del.yml
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=('POST',), strict_slashes=False)
def users_post():
    """
    file: ./swag/users_post.yml
    """
    http_dict = request.get_json()
    if not http_dict:
        return make_response(jsonify(error='Not a JSON'), 400)
    if 'email' not in http_dict.keys():
        return make_response(jsonify(error='Missing email'), 400)
    if 'password' not in http_dict.keys():
        return make_response(jsonify(error='Missing password'), 400)
    user = User(**http_dict)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=('PUT',), strict_slashes=False)
def users_put(user_id=None):
    """
    file: ./swag/users_put.yml
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        return make_response(jsonify(error='Not a JSON'), 400)
    for key, value in http_dict.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
