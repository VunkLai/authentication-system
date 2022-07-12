from pathlib import Path
from typing import Optional

from django.contrib.auth.models import User
from django.utils import timezone

import jwt

folder = Path('/etc/ssl/authentication.system')


def sign(user: User) -> str:
    with open(folder / 'private.pem', 'r', encoding='utf-8') as fr:
        private_key = fr.read().encode()
    now = timezone.localtime()
    payload = {
        'username': user.username,
        'email': user.email,
        'permissions': list(user.get_all_permissions()),
        'exp': now + timezone.timedelta(hours=2),
    }
    return jwt.encode(payload, private_key, algorithm='RS256')


def verify(token: str) -> Optional[User]:
    with open(folder / 'public.pem', 'r', encoding='utf-8') as fr:
        public_key = fr.read().encode()
    try:
        payload = jwt.decode(token, public_key, algorithms='RS256')
        return User.objects.get(username=payload['username'])
    except jwt.exceptions.InvalidTokenError:
        return None
    except User.DoesNotExist:
        return None
