

class HookManager(object):
    """A registry for storing and retrieving hooks"""

    _hooks = {}

    def register(self, hook, hook_name):
        existing_hooks = self._hooks.setdefault(hook_name, [])
        if not hook in existing_hooks:
            existing_hooks.append(hook)

    def get(self, hook_name):
        return self._hooks.get(hook_name, [])
