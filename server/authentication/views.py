from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def forgot_password(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


def reset_password(request: HttpRequest, hash_link: str) -> HttpResponse:
    return HttpResponse()


def change_password(request: HttpRequest) -> HttpResponse:
    return HttpResponse()
