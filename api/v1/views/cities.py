#!/usr/bin/python3
"""
Citys View
"""

from . import app_views
from models import storage
from models.city import City
from ...import jsonify
from flask import abort, request


@app_views.route("/amenities/<uuid:state_id>/cities", strict_slashes=False,
                 methods=["GET", "POST"])
def cities_by_state(state_id):
    """create and retrieve cities"""
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])
    if request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing name"}, status=400)
        city = City(**data, state_id=state.id)
        city.save()
        return jsonify(city.to_dict(), status=201)


@app_views.route("/cities/<uuid:city_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_delete_update_cities(city_id):
    """get, delete and update a city"""
    city = storage.get("City", str(city_id))
    print("city:", city, "city_id:", city_id)
    if not city:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        for k, v in data.items():
            if k in ("id", "created_at", "updated_at", "state_id"):
                continue
            setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
