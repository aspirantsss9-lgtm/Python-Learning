from django.http import HttpResponse


def index(request):
    """Return a simple application response."""
    return HttpResponse("DjangoStore is running.")