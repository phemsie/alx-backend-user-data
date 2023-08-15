#!/usr/bin/env python3
"""
End-to-end integration test module.
"""
from requests import get, put, post, delete

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    # New user successfully created
    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    print("Actual Response:", response)  # Debugging print statement
    assert response == {"email": email, "message": "user created"}
    assert request.status_code == 200

    # Email already associated with user
    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    assert response == {"message": "email already registered"}
    assert request.status_code == 400

# ... (rest of the functions remain the same)

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
