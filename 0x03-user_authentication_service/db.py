#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user to the database
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None

        return user

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user from a given parameters
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()

        result = self.__session.query(User).filter(
            tuple_(*fields) == tuple(values)
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates user from given parameters
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        update_values = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_values[getattr(User, key)] = value
            else:
                raise ValueError()
        self.__session.query(User).filter(User.id == user_id).update(
            update_values,
            synchronize_session=False,
        )
        self._session.commit()
