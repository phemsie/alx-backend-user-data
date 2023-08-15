#!/usr/bin/env python3
"""
Authentication module.
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Class responsible for managing user authentication interactions with the database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.
        
        Args:
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            User: Instance of the created user.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided password is valid for the user.
        
        Args:
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            bool: True if the credentials are valid, otherwise False.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return False
        return True

    def create_session(self, email: str) -> str:
        """Creates a session for the user.
        
        Args:
            email (str): User's email.
            
        Returns:
            str: The created session ID.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id

    # ... (similar comments for other methods)

def _hash_password(password: str) -> bytes:
    """Hashes the provided password.
    
    Args:
        password (str): User's password.
        
    Returns:
        bytes: Hashed password.
    """
    e_pwd = password.encode()
    return bcrypt.hashpw(e_pwd, bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generates a unique UUID.
    
    Returns:
        str: Generated UUID.
    """
    return str(uuid4())
