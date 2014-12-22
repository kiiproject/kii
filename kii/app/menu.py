from django.core.urlresolvers import reverse



class MenuNode(object):
    """
    Describe a menu element, and may be attached to a :py:class:`App <kii.app.core.App>` instance
    (via the :py:attr:`menu <kii.app.core.App.menu>`) for automatic inclusion in templates.

    Nodes can be nested without limitation (a 42-levels menu seems pointless, though), using
    ``children`` attribute"""

    reverse_kwargs = []
    route = "#"
    parent = None
    weight = 0
    reverse = True
    require_authentication = True

    def __init__(self, **kwargs):

        self.reverse = kwargs.get('reverse', self.reverse)

        # a route that will be reversed if reverse is True
        self.route = kwargs.get('route', self.route)
        self.label = kwargs.get('label', self.route)
        self.parent = kwargs.get('parent', self.parent)        
        self.title = kwargs.get('title', self.label)
        self.weight = kwargs.get('weight', self.weight)
        self.require_authentication = kwargs.get('require_authentication', self.require_authentication)
        self.icon = kwargs.get('icon', None)

        self.reverse_kwargs = kwargs.get('reverse_kwargs', self.reverse_kwargs)

        self.children = []
        for item in kwargs.get('children', []):
            self.add(item)

    def url(self, **kwargs):
        if self.reverse :
            expected_kwargs = {key: value for key, value in kwargs.items() if key in self.reverse_kwargs}
            return reverse(self.route, kwargs=expected_kwargs)
        return self.route

    def add(self, item):
        self.children.append(item)
        self.children = sorted(self.children, key=lambda i: i.weight, reverse=True)

        



