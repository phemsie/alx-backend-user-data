#!/usr/bin/env python3
"""
Session authentication module that contains a class `SessionDBAuth` that
extends `api.v1.auth.auth.SessionExpAuth`
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """
    def create_session(self, user_id=None):
        """
        A method that overloads `api.v1.auth.auth.SessionExpAuth` and
        creates and stores a new instance of `UserSession` and returns
        the session ID.
        """
        if user_id:
            session_id = super().create_session(user_id)
            if session_id:
                user_session = UserSession(
                    user_id=user_id, session_id=session_id
                )
                user_session.save()
                return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        A method that overloads `api.v1.auth.auth.SessionExpAuth` and
        returns a user id from a database based on `session_id`
        """
        if session_id:
            UserSession.load_from_file()
            from models.base import DATA

            for item in DATA['UserSession'].values():
                self.user_id_by_session_id[item.session_id] = {
                    'user_id': item.user_id,
                    'created_at': item.created_at
                }
            user_id = super().user_id_for_session_id(session_id)
            return user_id  # NOTE: Will return None sometimes
        return None

    def destroy_session(self, request=None):
        """
        A method that overloads `api.v1.auth.auth.SessionExpAuth` and
        destroys the `UserSession` based on the session id from the
        request cookie.
        """
        if request:
            # Remove session ID from session dict
            destroyed = super().destroy_session(request)
            # Remove session ID from global DATA dict
            from models.base import DATA
            session_id = self.session_cookie(request)
            if session_id:
                for k, obj in DATA['UserSession'].items():
                    if obj.session_id == session_id:
                        del DATA['UserSession'][k]
                        UserSession.save_to_file()
                        break
            return destroyed
        return None
