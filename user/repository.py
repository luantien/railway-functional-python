# profile/service.py
from dataclasses import asdict
from typing import Dict
from datetime import datetime, timezone
import json

from common.decorator import railway_handler
from common.result import Failure
from monitoring.exception import DataException, ServerException
from user.model import User


USER_DATA_SOURCE = "temp/user__{}.json"

@railway_handler(ServerException, DataException)
def create_user(user: User) -> User:
    """Saves data to a database and returns the saved User with ID."""
    if not user.id:
        raise DataException("User ID is missing.")
    if user.scenario == "timeout":
        raise ServerException("Database connection timed out.")

    return save_user(user)


@railway_handler()
def get_user_by_id(user_id: str) -> User:
    """Loads user data from a database through its ID."""
    with open(USER_DATA_SOURCE.format(user_id), "r") as f:
        data = json.load(f)
        print(f"✅ Retrieved user data with ID: {user_id}")
        return User(**data)


@railway_handler()
def save_user(user: User) -> User:
    """Saves user data to a database."""
    try:
        with open(USER_DATA_SOURCE.format(user.id), "w") as f:
            f.write(json.dumps(asdict(user)))
    except Exception as e:
        raise ServerException("Failed to save user data: " + str(e))
    print(f"✅ User updated with ID: {user.id}")
    return user


@railway_handler()
def update_user(updating_user: User) -> User:
    """Updates an existing user's profile."""
    def merge_user_data(user: User) -> User:
        """Merges existing user data with the new data."""
        user += updating_user
        return user

    return get_user_by_id(updating_user.id).map(merge_user_data).and_then(save_user)
