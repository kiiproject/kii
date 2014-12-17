from django.http import HttpResponse


def blank(*args, **kwargs):
    "a blank view, for use in URLconf"
    return HttpResponse('')