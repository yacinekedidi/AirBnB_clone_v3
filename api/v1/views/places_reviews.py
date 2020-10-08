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


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_of_a_place(place_id):
    """
    file: review_get.yml
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_get(review_id):
    """
    file: review_get_by_id.yml
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_del(review_id):
    """
    file: review_delete.yml
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_post(place_id=None):
    """
    file: review_post.yml
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    if 'user_id' not in http_dict.keys():
        abort(400, description='Missing user_id')
    if not storage.get(User, http_dict['user_id']):
        abort(404)
    if 'text' not in http_dict.keys():
        abort(400, description='Missing text')
    review = Review(**http_dict)
    setattr(review, "place_id", place_id)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """
    file: review_put.yml
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    http_dict = request.get_json()
    if not http_dict:
        abort(400, description='Not a JSON')
    for key, value in http_dict.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
