from typing import Optional, Tuple
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from apps.accounts.repositories.user_repository import UserRepository


class AuthService:
    """
    Business logic layer for user accounts and authentication.
    """

    def __init__(self, user_repo: Optional[UserRepository] = None):
        self.user_repo = user_repo or UserRepository()

    def register_user(self, username: str, password: str, email: str = '') -> User:
        """
        Creates a new user using the user repository.
        """
        return self.user_repo.create_user(
            username=username,
            password=password,
            email=email
        )

    def authenticate_user(self, request, username: str, password: str) -> Optional[User]:
        """
        Validates credentials and returns User if valid, None otherwise.
        """
        return authenticate(request, username=username, password=password)
