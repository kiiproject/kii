#!/usr/bin/env python
import sys

from django.conf import settings

from kii.tests import settings as test_settings


if __name__ == "__main__":
    settings.configure(
        test_settings,
        INSTALLED_APPS=test_settings.INSTALLED_APPS + ('kii_snippets.apps.App',) # NOQA
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
