#!/usr/bin/python3
"""
States View
"""

from . import app_views
from models import storage
from models.state import State
from ...import jsonify
from flask import abort, request


@app_views.route("/states/", strict_slashes=False,
                 defaults={'state_id': None}, methods=["POST", "GET"])
@app_views.route("/states/<uuid:state_id>", strict_slashes=False,
                 methods=["GET", "PUT", "DELETE"])
def get_all_states(state_id):
    """retrieve all states"""
    if state_id:
        state_id = str(state_id)
    if request.method == "GET":
        if state_id:
            state = storage.get("State", state_id)
            if not state:
                abort(404)
            return jsonify(state.to_dict())
        return jsonify([
            obj.to_dict() for obj in storage.all("State").values()
        ])
    elif request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing name"}, status=400)
        state = State(**data)
        state.save()
        return jsonify(state.to_dict(), status=201)
    elif request.method == "PUT":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}, status=400)
        data = request.get_json()
        state = storage.get("State", state_id) if state_id else None
        if not state:
            abort(404)
        for k, v in data.items():
            if k in ("id", "created_at", "updated_at"):
                continue
            setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        state = storage.get("State", state_id) if state_id else None
        if not state:
            abort(404)
        state.delete()
        storage.save()
        return jsonify({})
