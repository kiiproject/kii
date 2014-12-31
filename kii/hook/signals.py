import django.dispatch


def InstanceSignal(providing_args=[]):
    """Return a Signal instance that will always send an instance argument,
    and provided args
    """

    args = ['instance'] + providing_args

    return django.dispatch.Signal(providing_args=args)
