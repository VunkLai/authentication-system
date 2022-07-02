from django.contrib.auth.models import User

import pytest
from authentication.jwt import sign, verify


@pytest.mark.django_db
def test_sign():
    user = User.objects.create(username='username')
    token = sign(user)
    assert isinstance(token, str)


@pytest.mark.django_db
def test_verify():
    user = User.objects.create(username='username')
    token = sign(user)

    valid_user = verify(token)
    assert valid_user == user
