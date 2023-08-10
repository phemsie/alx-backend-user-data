#!/usr/bin/env python3
""" Flask view that handles all routes for the Session authentication
"""
from flask import jsonify, abort, request
import os
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ handles all routes for session authentication
    """
    user_email = request.form.get('email')
    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password')
    if pwd is None or pwd == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            jsonified_user = jsonify(user.to_json())
            jsonified_user.set_cookie(os.getenv('SESSION_NAME'), session_id)
