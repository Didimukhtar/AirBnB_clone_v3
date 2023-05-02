#!/usr/bin/python3
"""
AirBnB API definition
"""
from flask import Flask
from .views import app_views
from .. import jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    storage.close()


@app.errorhandler(404)
def on_404_error(e):
    return jsonify({"error": "Not found"}, status=404)


if __name__ == "__main__":
    import os

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True)
