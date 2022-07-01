from typing import Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

import jwt


def sign(user: User) -> str:
    now = timezone.localtime()
    payload = {
        'username': user.username,
        'permissions': list(user.get_all_permissions()),
        'exp': now + timezone.timedelta(hours=2),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


def verify(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        return User.objects.get(username=payload['username'])
    except jwt.exceptions.InvalidTokenError:
        return None
    except User.DoesNotExist:
        return None
