from functools import wraps
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.loader import get_template

from authentication import jwt
from authentication.models import ForgotPassword


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


@request_validator
def login(request: HttpRequest) -> HttpResponse:
    username = request.json['username']
    password = request.json['password']
    user = authenticate(username=username, password=password)
    if user:
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'access-token': jwt.sign(user),
        })
    return HttpResponse(
        'Incorrect username or password.',
        status=HTTPStatus.UNAUTHORIZED
    )


@request_validator
def forgot_password(request: HttpRequest) -> HttpResponse:
    username = request.json['username']
    try:
        user = User.objects.get(username=username)
        record = ForgotPassword.objects.create(user)
        # send an email to the user
        if settings.STAGE == 'production':
            template = get_template('forgot_password_email.html')
            context = {
                'url': f'http://{settings.URL}/{record.hash_link}'
            }
            content = template.render(context)
            user.email_user(subject='Password reset request', html_message=content)
        return JsonResponse({'message': 'ok'})
    except User.DoesNotExist:
        return HttpResponse(
            'The username does not exist.',
            status=HTTPStatus.BAD_REQUEST
        )


def reset_password(request: HttpRequest, hash_link: str) -> HttpResponse:
    try:
        record = ForgotPassword.objects.get(hash_link=hash_link, done=False)
        if record.is_expired:
            return HttpResponse(
                'This link expired',
                status=HTTPStatus.NOT_FOUND
            )
        password = request.json['password']
        record.reset_password(password)
        return JsonResponse({'message': 'ok'})
    except ForgotPassword.DoesNotExist:
        return HttpResponse(
            'Not Found',
            status=HTTPStatus.NOT_FOUND
        )
    except KeyError:
        return HttpResponse(
            'Invalid Request.',
            status=HTTPStatus.BAD_REQUEST
        )


@request_validator
def change_password(request: HttpRequest) -> HttpResponse:
    password = request.json['password']
    request.user.set_password(password)
    request.user.save()
    return JsonResponse({'message': 'ok'})
