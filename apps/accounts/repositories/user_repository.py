from typing import Optional
from django.contrib.auth.models import User


class UserRepository:
    """
    Encapsulates all database interactions for User model.
    """

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        try:
            return User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def exists_by_username(username: str) -> bool:
        return User.objects.filter(username__iexact=username).exists()

    @staticmethod
    def exists_by_email(email: str) -> bool:
        if not email:
            return False
        return User.objects.filter(email__iexact=email).exists()

    @staticmethod
    def create_user(username: str, password: str, email: str = '', first_name: str = '', last_name: str = '') -> User:
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
