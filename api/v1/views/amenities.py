#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>',
                 methods=('GET',), strict_slashes=False)
@app_views.route('/amenities', methods=('GET',), strict_slashes=False)
def amenities_get(amenity_id=None):
    """
    file: ./swag/amenities_get.yml
    """
    if not amenity_id:
        obj_list = []
        for key, obj in storage.all("Amenity").items():
            obj_list.append(obj.to_dict())
        return jsonify(obj_list)
    else:
        amenit = storage.get(Amenity, amenity_id)
        if not amenit:
            abort(404)
        else:
            return jsonify(amenit.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=('DELETE',),
                 strict_slashes=False)
def amenities_del(amenity_id=None):
    """
    file: ./swag/amenities_del.yml
    """
    amenit = storage.get(Amenity, amenity_id)
    if not amenit:
        abort(404)
    else:
        storage.delete(amenit)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=('POST',), strict_slashes=False)
def amenities_post():
    """
    file: ./swag/amenities_post.yml
    """
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    if 'name' not in http_dict.keys():
        abort(400, description='Missing name')
    amenit = Amenity(**http_dict)
    storage.new(amenit)
    storage.save()
    return make_response(jsonify(amenit.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=('PUT',), strict_slashes=False)
def amenities_put(amenity_id=None):
    """
    file: ./swag/amenities_put.yml
    """
    amenit = storage.get(Amenity, amenity_id)
    if not amenit:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    for key, value in http_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenit, key, value)
    storage.save()
    return make_response(jsonify(amenit.to_dict()), 200)
