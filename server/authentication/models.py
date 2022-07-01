from __future__ import annotations

import os
from hashlib import blake2b

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def generate_hash_link(username: str) -> str:
    msg = username.encode()
    salt = os.urandom(blake2b.SALT_SIZE)
    encryption = blake2b(salt=salt, digest_size=32)
    for _ in range(settings.ITERATIONS):
        encryption.update(msg)
    return encryption.hexdigest()


class ForgotPasswordManager(models.Manager):

    def create(self, user: User) -> ForgotPassword:
        hash_link = generate_hash_link(user.username)
        return super().create(user=user, hash_link=hash_link, done=False)


class ForgotPassword(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_link = models.CharField(max_length=64, unique=True)
    done = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ForgotPasswordManager()
