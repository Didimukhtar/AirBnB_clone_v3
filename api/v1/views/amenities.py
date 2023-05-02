#!/usr/bin/python3
"""
Amenities View
"""

from . import app_views
from models import storage
from models.amenity import Amenity
from ...import jsonify
from flask import abort, request


@app_views.route("/amenities/", strict_slashes=False,
                 defaults={'amenity_id': None}, methods=["POST", "GET"])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET", "PUT", "DELETE"])
def get_all_amenitys(amenity_id):
    """
    retrieve all amenities snfnjnjkwndf nfejn mdz jfnjknsjn jdnkjnfdsn
    """
    if amenity_id:
        amenity_id = str(amenity_id)
    if request.method == "GET":
        if amenity_id:
            amenity = storage.get("Amenity", amenity_id)
            if not amenity:
                abort(404)
            return jsonify(amenity.to_dict())
        return jsonify([
            obj.to_dict() for obj in storage.all("Amenity").values()
        ])
    elif request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing name"}, status=400)
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict(), status=201)
    elif request.method == "PUT":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        amenity = storage.get("Amenity", amenity_id) if state_id else None
        if not amenity:
            abort(404)
        for k, v in data.items():
            if k in ("id", "created_at", "updated_at"):
                continue
            setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        amenity = storage.get("Amenity", amenity_id) if state_id else None
        if not amenity:
            abort(404)
        amenity.delete()
        storage.save()
        return jsonify({})
