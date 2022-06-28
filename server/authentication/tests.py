from authentication import views


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
        assert response.status_code == 200
