from http import HTTPStatus

import pytest

PATH = '/auth/login'
FORM = {'username': 'username', 'password': 'password'}


@pytest.mark.django_db
def test_login(client):
    response = client.post('/auth/register', data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(PATH, data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.OK, response.content

    body = response.json()
    assert 'username' in body
    assert 'email' in body
    assert 'access-token' in body


@pytest.mark.django_db
def test_wrong_username(client):
    response = client.post('/auth/register', data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED

    fake_data = {'username': 'fake-name', 'password': FORM['password']}
    response = client.post(PATH, data=fake_data, content_type='application/json')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content


@pytest.mark.django_db
def test_wrong_password(client):
    response = client.post('/auth/register', data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED

    fake_data = {'username': FORM['username'], 'password': 'fake-password'}
    response = client.post(PATH, data=fake_data, content_type='application/json')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content
