import json
from http import HTTPStatus
from typing import Callable

from django.http import HttpRequest, HttpResponse

from authentication.jwt import verify


class JsonRequestMiddleware:

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not request.content_type == 'application/json':
            return HttpResponse(
                'Invalid Content-type.',
                status=HTTPStatus.NOT_ACCEPTABLE
            )
        try:
            request.json = json.loads(request.body)
            response = self.get_response(request)
            return response
        except json.decoder.JSONDecodeError:
            return HttpResponse(
                'Invalid JSON format.',
                status=HTTPStatus.BAD_REQUEST
            )


class AuthenticationMiddleware:

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.paths = [
            '/auth/change-password',
        ]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path not in self.paths:
            response = self.get_response(request)
            return response

        try:
            _, token = request.headers['Authorization'].split(' ', 1)
            user = verify(token)
            if user:
                request.user = user
                response = self.get_response(request)
                return response
            return HttpResponse(
                'Invalid token.',
                status=HTTPStatus.FORBIDDEN
            )
        except KeyError:
            return HttpResponse(
                'Token not found.',
                status=HTTPStatus.FORBIDDEN
            )
