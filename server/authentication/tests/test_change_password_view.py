from http import HTTPStatus

import pytest

FORM = {
    'username': 'username',
    'password': 'password'
}


@pytest.mark.django_db
def test_change_password(client):
    client.post('/auth/register', data=FORM, content_type='application/json')
    response = client.post('/auth/login', data=FORM, content_type='application/json')
    token = response.json().get('access-token')
    assert token

    new_password = {'password': 'new-password'}
    response = client.post(
        '/auth/change-password',
        data=new_password,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )
    assert response.status_code == HTTPStatus.OK

    login = {
        'username': FORM['username'],
        'password': new_password['password'],
    }
    response = client.post('/auth/login', data=login, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
