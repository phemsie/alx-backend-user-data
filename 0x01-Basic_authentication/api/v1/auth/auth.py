#!/usr/bin/env python3
""" module of api authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """ manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None,
        request will be the Flask request object
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None,
        request will be the Flask request object
        """
        return None
