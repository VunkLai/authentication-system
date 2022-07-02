from http import HTTPStatus

import pytest
from authentication.models import ForgotPassword

FORM = {
    'username': 'username',
    'password': 'password',
}


@pytest.mark.django_db
def test_reset_password(client):
    response = client.post('/auth/register', data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED

    response = client.post('/auth/forgot-password', data={'username': 'username'}, content_type='application/json')
    assert response.status_code == HTTPStatus.OK

    # get link from email
    record = ForgotPassword.objects.first()

    response = client.post(
        f'/auth/reset-password/{record.hash_link}',
        data={'password': 'new-password'},
        content_type='application/json'
    )
    assert response.status_code == HTTPStatus.OK

    login = {'username': 'username', 'password': 'new-password'}
    response = client.post('/auth/login', data=login, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
