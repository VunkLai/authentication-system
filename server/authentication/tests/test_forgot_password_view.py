from http import HTTPStatus

from django.contrib.auth.models import User

import pytest
from authentication.models import ForgotPassword

FORM = {
    'username': 'username',
    'password': 'password',
}


@pytest.mark.django_db
def test_forgot_password(client):
    response = client.post('/auth/register', data=FORM, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED

    response = client.post('/auth/forgot-password', data={'username': 'username'}, content_type='application/json')
    assert response.status_code == HTTPStatus.OK

    # get hash-link from email
    user = User.objects.get(username=FORM['username'])
    records = ForgotPassword.objects.filter(user=user)
    assert records.exists()


@pytest.mark.django_db
def test_forgot_password_with_wrong_user(client):
    wrong_user = {
        'username': FORM['username'],
    }
    response = client.post('/auth/forgot-password', data=wrong_user, content_type='application/json')

    assert response.status_code == HTTPStatus.BAD_REQUEST
