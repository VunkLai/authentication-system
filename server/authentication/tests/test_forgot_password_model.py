from django.conf import settings
from django.contrib.auth.models import User

import pytest
from authentication import models


def test_settings_has_iterations():
    assert settings.ITERATIONS
    assert isinstance(settings.ITERATIONS, int)
    assert settings.ITERATIONS >= 16


def test_settings_has_url():
    assert settings.URL
    assert isinstance(settings.URL, str)


def test_settings_has_stage():
    assert settings.STAGE
    assert settings.STAGE in ['development', 'production']


def test_generate_hash_link():
    username = 'username'
    link = models.generate_hash_link(username)
    assert isinstance(link, str)
    assert len(link) == 64


def test_should_not_generate_duplicate_link():
    username = 'username'
    link1 = models.generate_hash_link(username)
    link2 = models.generate_hash_link(username)
    assert link1 != link2


@pytest.mark.django_db
def test_manager_create():
    user = User.objects.create(username='username', password='password')
    record = models.ForgotPassword.objects.create(user)
    assert record.user == user
    assert len(record.hash_link) == 64
    assert not record.done
