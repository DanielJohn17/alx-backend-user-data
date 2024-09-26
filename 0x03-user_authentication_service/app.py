#!/usr/bin/env python3
""" API module
"""
from flask import Flask, jsonify, request

from auth import Auth


app = Flask(__name__)
AUTH = Auth()
app.url_map.strict_slashes = False


@app.route("/", methods=["GET"])
def home() -> str:
    """ Main page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """POST /users
    Return:
        - The account creation payload.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
