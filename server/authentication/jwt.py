from typing import Optional

from django.contrib.auth.models import User


def sign(user: User) -> str:
    return ''


def verify(token: str) -> Optional[User]:
    return None
