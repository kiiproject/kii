from django.core.urlresolvers import reverse



class MenuItem(object):
    """Used to describe menu elements"""


    def __init__(self, **kwargs):

        # a route that will be reversed
        self.route = kwargs.get('route', "#")
        self.label = kwargs.get('label', self.route)
        self.parent = kwargs.get('parent', None)        
        self.title = kwargs.get('title', self.label)
        self.weight = kwargs.get('weight', 0)


    def path(self, **kwargs):
        if self.route == "#":
            return self.route
        return reverse(self.route, kwargs=kwargs)


class Menu(MenuItem):
    """A MenuItem that can have children"""

    def __init__(self, **kwargs):

        super(Menu, self).__init__(**kwargs)   
        self.children = []
        for item in kwargs.get('children', []):
            self.add(item)

    def add(self, item):
        self.children.append(item)
        self.children = sorted(self.children, key=lambda i: i.weight, reverse=True)


