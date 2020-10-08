#!/usr/bin/python3
"""
starts a Flask web application
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify
from models import storage
from flask_cors import CORS
from flasgger import Swagger
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
swagger = Swagger(app)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found_404(e):
    """a handler for 404 errors that returns
    a JSON-formatted 404 status code response
    """
    resp = make_response(jsonify(error="Not found"), 404)
    return resp


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"),
            threaded=True)
