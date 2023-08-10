#!/usr/bin/env python3
""" Basic auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[0:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64.b64encode(base64.b64decode(
                base64_authorization_header)) == base64_authorization_header
        except BaseException:
            return None
        return base64.b64decode(
            base64_authorization_header + '===').decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns the user emain and password from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        lst = decoded_base64_authorization_header.split(":")
        return lst[0], lst[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ return the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except BaseException:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User
        instance of a request
        """
        try:
            authHeader = self.authorization_header(request)
            b64Header = self.extract_base64_authorization_header(authHeader)
            decodedStr = self.decode_base64_authorization_header(b64Header)
            userCredentials = self.extract_user_credentials(decodedStr)
            user = self.user_object_from_credentials(
                            userCredentials[0], userCredentials[1])
            return user
        except BaseException:
            return None
