from http import HTTPStatus

from django.contrib.auth.models import User

import pytest

PATH = '/auth/register'
FORM = {'username': 'username', 'password': 'password'}


@pytest.mark.django_db
def test_register(client, settings):
    response = client.post(PATH, data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED, response.content
    assert 'user_id' in response.json(), response.content

    user = User.objects.get(username=FORM['username'])
    assert user.email == f'{FORM["username"]}@{settings.DOMAIN}'


@pytest.mark.django_db
def test_register_with_duplicate_username(client):
    response = client.post(PATH, data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED, response.content

    response = client.post(PATH, data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.content


def test_register_post_only(client):
    response = client.put(PATH, data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, response.content


def test_register_allows_only_json_request(client):
    response = client.post(PATH, data=FORM)
    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE, response.content


def test_register_returns_bad_request(client):
    response = client.post(PATH, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.content

    form = {'username': 'username'}
    response = client.post(PATH, data=form, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.content

    form = {'password': 'password'}
    response = client.post(PATH, data=form, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.content
