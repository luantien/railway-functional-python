# user/use_case.py
from typing import Dict

from common.decorator import railway_handler
from monitoring.exception import DataException
from user.model import User
from user.repository import create_user, get_user_by_id, update_user


@railway_handler()
def validate_user_data(raw_data: Dict) -> User:
    """Validates user data."""
    if "name" not in raw_data or len(raw_data["name"]) <= 2:
        raise DataException("User name is invalid.")
    print("✅ Validated user data ...")
    return User(**raw_data)


@railway_handler()
def process_new_user(raw_data: Dict) -> User:
    """Validates then persist user data and returns a User."""
    return validate_user_data(raw_data).and_then(create_user)


@railway_handler()
def retrieve_user_profile(user_id: str) -> User:
    """Loads user profile from the database."""
    return get_user_by_id(user_id)


@railway_handler()
def process_existing_user(user_id: str, user_data: Dict) -> User:
    """Updates an existing user's profile."""
    user_data["id"] = user_id
    return validate_user_data(user_data).and_then(update_user)
