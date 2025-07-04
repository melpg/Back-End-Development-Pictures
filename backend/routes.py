from . import app
import os
import json

from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return jsonify({"message": "No pictures found"}), 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    
    if not picture:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Check if picture with the given id already exists
    for pic in data:
        if pic.get("id") == picture.get("id"):
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()
    
    if not updated_picture:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Find the picture in the data list
    for index, pic in enumerate(data):
        if pic.get("id") == id:
            # Update the existing picture with new data
            updated_picture["id"] = id  # ensure id remains same
            data[index] = updated_picture
            return jsonify(updated_picture), 200

    # If picture not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, pic in enumerate(data):
        if pic.get("id") == id:
            # Delete the picture from the list
            del data[index]
            return '', 204  # Empty body with 204 No Content

    # If picture not found
    return jsonify({"message": "picture not found"}), 404
