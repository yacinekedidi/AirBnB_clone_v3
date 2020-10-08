#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=('GET',), strict_slashes=False)
def status():
    """ Returns a JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=('GET',), strict_slashes=False)
def stats():
    """ Retrieves the number of each objects by type """
    obj_types = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"}
    dt = {}
    for key, obj in obj_types.items():
        dt[key] = storage.count(obj)
    return jsonify(dt)
