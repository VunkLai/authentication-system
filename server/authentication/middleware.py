import json
from http import HTTPStatus
from typing import Callable

from django.http import HttpRequest, HttpResponse


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
