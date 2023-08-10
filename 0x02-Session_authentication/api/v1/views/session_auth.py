#!/usr/bin/env python3
"""
A module that contains a flask view that handles all routes for session
authentication
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ A view that authenticates a user session """
    email = request.form.get('email')
    passwd = request.form.get('password')
    if email in [None, ""]:
        return jsonify({"error": "email missing"}), 400
    if passwd in [None, ""]:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if users:
        user = users[0]
        if user.is_valid_password(passwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = make_response(user.to_json(), 200)
            SESSION_NAME = os.getenv('SESSION_NAME')
            if SESSION_NAME:
                resp.set_cookie(SESSION_NAME, session_id)
            return resp  # Returns response whether cookie is set or not
        else:
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ a view that implements Logout function """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
