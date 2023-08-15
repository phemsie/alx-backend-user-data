#!/usr/bin/env python3
"""
Flask app for user authentication and profile management.
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()

@app.route("/")
def home() -> str:
    """Endpoint for the home page.
    
    Returns:
        str: A JSON representation of a welcome message.
    """
    return jsonify({"message": "Welcome"})

@app.route("/sessions", methods=["POST"])
def login():
    """Endpoint for user login.
    
    Form fields:
        - email
        - password
        
    Returns:
        Response: User's email and login message if successful, 401 if credentials are invalid.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "Logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"])
def logout():
    """Endpoint for user logout.
    
    Returns:
        Response: Redirects to the home page after logging out.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))

@app.route("/users", methods=["POST"])
def users():
    """Endpoint for new user registration.
    
    Form fields:
        - email
        - password
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "User created"})
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400

@app.route("/profile")
def profile() -> str:
    """Endpoint for user profile information.
    
    Returns:
        Response: User's email if authenticated, 403 if session is invalid.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})

@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """Endpoint to request a reset password token.
    
    Form fields:
        - email
        
    Returns:
        Response: User's email and reset token if successful, 403 if email is not associated with any user.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})

@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Endpoint to update user password using a reset token.
    
    Form fields:
        - email
        - reset_token
        - new_password
        
    Returns:
        Response: User's email and password update message if successful, 403 if reset token is invalid.
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
