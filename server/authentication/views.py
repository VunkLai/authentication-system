from functools import wraps
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse


def request_validator(func_view):
    @wraps(func_view)
    def wrapper(request, *args, **kwargs):
        if not request.method == 'POST':
            return HttpResponse(
                'Method Not Allowed',
                status=HTTPStatus.METHOD_NOT_ALLOWED
            )
        try:
            return func_view(request, *args, **kwargs)
        except KeyError:
            return HttpResponse(
                'Invalid Request.',
                status=HTTPStatus.BAD_REQUEST
            )
    return wrapper


@request_validator
def register(request: HttpRequest) -> HttpResponse:
    username = request.json['username']
    password = request.json['password']
    email = f'{username}@{settings.DOMAIN}'
    try:
        user = User.objects.create_user(username, email=email, password=password)
        return JsonResponse({'user_id': user.id}, status=HTTPStatus.CREATED)
    except IntegrityError:
        return HttpResponse(
            'The username you specified is already in use.',
            status=HTTPStatus.BAD_REQUEST
        )


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def forgot_password(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def reset_password(request: HttpRequest, hash_link: str) -> HttpResponse:
    return HttpResponse()


def change_password(request: HttpRequest) -> HttpResponse:
    return HttpResponse()
