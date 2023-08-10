#!/usr/bin/env python3
"""
Session authentication module that contains a class `SessionAuth` that
extends `api.v1.auth.auth.Auth`
"""
from .auth import Auth
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ A class that implements session authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ A method that creates a session id for a user_id """
        if user_id and type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ A method that returns user id based on a session id """
        if session_id and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """ A method that overloads and returns a user instance based on a
        cookie value """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_id = self.user_id_for_session_id(session_id)
                if user_id:
                    user = User.get(user_id)
                    return user
        return None

    def destroy_session(self, request=None):
        """ A method that deletes the user session (logout function) """
        if request:
            session_id = self.session_cookie(request)
            if session_id and self.user_id_for_session_id(session_id):
                del self.user_id_by_session_id[session_id]
                return True
        return False
