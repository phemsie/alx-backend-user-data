#!/usr/bin/env python3
"""
Encrypting password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a hashed password"""
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates that provided password matches
    the hashed password"""
    if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
        return True
    return False
