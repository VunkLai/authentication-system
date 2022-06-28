

from http import HTTPStatus


def test_all_routes(client):
    routes = [
        '/auth/register',
        '/auth/login',
        '/auth/forgot-password',
        '/auth/reset-password/hash-link',
        '/auth/change-password',
    ]
    for route in routes:
        response = client.get(route)
        assert response.status_code == HTTPStatus.NOT_ACCEPTABLE


def test_json_request_middleware(client):
    routes = [
        '/auth/register',
        '/auth/login',
        '/auth/forgot-password',
        '/auth/reset-password/hash-link',
        '/auth/change-password',
    ]
    for route in routes:
        response = client.post(route, content_type='application/json')
        assert response.status_code == HTTPStatus.OK
