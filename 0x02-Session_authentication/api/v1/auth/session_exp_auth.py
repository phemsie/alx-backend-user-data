#!/usr/bin/env python3
"""
Session authentication module that contains a class `SessionExpAuth` that
extends `api.v1.auth.auth.SessionAuth`
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ A class that implements an expirable session. """
    def __init__(self):
        """ Initialization """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        A method that overloads `SessionAuth.create_session` by adding a
        `session dictionary` containing `user_id` and `date created`.
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        A method that overloads `SessionAuth.user_id_for_session_id` by
        implementing session timeout
        """
        if session_id and type(session_id) is str:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                if self.session_duration <= 0:  # Sessns won't exp
                    return session_dict.get('user_id')
                else:  # Sessions will expire
                    created_at = session_dict.get('created_at')
                    if created_at:
                        c = created_at
                        created_at_delta = timedelta(
                            c.day, c.second, c.microsecond,
                            c.minute, c.hour
                        )
                        now = datetime.now()
                        now_delta = timedelta(
                            now.day, now.second, now.microsecond,
                            now.minute, now.hour
                        )
                        sess_d_delta = timedelta(seconds=self.session_duration)
                        # print('Before check')
                        if (created_at_delta + sess_d_delta) < now_delta:
                            # print('Session Expired')
                            return None
                        return session_dict.get('user_id')
        return None
