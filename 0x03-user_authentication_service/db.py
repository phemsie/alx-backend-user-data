#!/usr/bin/env python3
"""Database module for user authentication."""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User

class DB:
    """Database interface class for user authentication."""

    def __init__(self) -> None:
        """Initialize a new instance of the database."""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for efficient database access."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        
        Args:
            email (str): User's email.
            hashed_password (str): Hashed password.
            
        Returns:
            User: Newly created User object.
        """
        session = self._session
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
        except Exception:
            session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by specified attributes.
        
        Args:
            kwargs (dict): Dictionary of attributes to use as search parameters.
            
        Returns:
            User: User object matching the search criteria.
        
        Raises:
            InvalidRequestError: If an invalid attribute is used for searching.
            NoResultFound: If no user is found matching the search criteria.
        """
        attrs, vals = [], []
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            attrs.append(getattr(User, attr))
            vals.append(val)

        session = self._session
        query = session.query(User)
        user = query.filter(tuple_(*attrs).in_([tuple(vals)])).first()
        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes based on the provided user_id.
        
        Args:
            user_id (int): User's ID.
            kwargs (dict): Dictionary of attributes to update.
        
        Raises:
            ValueError: If an invalid attribute is provided for updating.
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError
            setattr(user, attr, val)
        session.commit()
