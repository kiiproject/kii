Upgrade instructions
====================

0.8
***

With the new file model, users can upload files in their streams. You'll have to create a ``media`` directory on your server in order to store these files.

Ensure the directory is writable by the user running kii, and edit your settings accordingly:

..code-block:: python
    
    # URL for user uploaded files, you should not have to touch this
    MEDIA_URL = '/media/'

    # Ensure this path is readable and writable by the webserver
    MEDIA_ROOT = "/path/to/your/media/directory"