#!/usr/bin/python3
"""
Index view
"""
from . import app_views
from models import storage
from ... import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """view the app status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """view the app stats"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    })
