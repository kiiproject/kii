

class ModelFilters(object):
    """A registry for storing filters that will be called when model fields are accessed via Model.filtered_<field_name>"""

    _hooks = {}

    def register(self, model, field_name, filter_func):
        """Register given filter function on given field name for given model"""
        model_hooks = self._hooks.setdefault(model, {})
        field_hooks = model_hooks.setdefault(field_name, [])

        if not filter_func in field_hooks:
            field_hooks.append(filter_func)

    def get(self, model, field_name):
        """ return a list of registered filters for given model and field_name"""
        model_hooks = self._hooks.get(model, None)
        if model_hooks is not None:
            return model_hooks.get(field_name, [])
        return []

    def filter(self, field_name, instance):        
        """Return the filtered value of given field on given instance"""

        filtered_value = getattr(instance, field_name)

        for filter_func in self.get(instance.__class__, field_name):
            filtered_value = filter_func(filtered_value, instance=instance)

        return filtered_value

    def clear(self):
        self._hooks.clear()

model_filters = ModelFilters()