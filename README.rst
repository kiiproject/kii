Installation
############

Create a new user for your kii instance::

    sudo adduser kii --disabled-login
    sudo su - kii

    cd ~

Create a virtualenvironment::

    pip install --user virtualenv
    virtualenv ./kii-virtualenv

Work on it::

    source ./kii-virtualenv

Then install required packages (PyPi install will be available soon)::

    pip install git+https://code.eliotberriot.com/kii/kii.git

Now, you can create a new kii instance using the built-in template::

    # replace pythonX.X by your own python version
    django-admin.py startproject kii_instance --template=./kii-virtualenv/lib/pythonX.X/site-packages/kii/install/instance_template

    cd kii_instance

It should create a kii_instance directory, with almost everything set up to make put your new kii instance online.

You can now adapt the settings under `kii_instance/settings.py` to suit your needs. For exemple, you will need to set your database credentials, your installed apps, etc. The settings file is heavily commented so I won't detail everything here.

When you're done, you can initialize the database with::

    python manage.py syncdb


Install kii apps
################

As Kii is not bundled with any app, you app to install these separately. Each app may have custom installation instruction, but most of the process will remain identical:

1. Download the app python packages (via `pip install`)
2. Open `kii_instance/settings.py`
3. Add the app name under `INSTALLED_APPS`
4. (optional) in the same file, add custom settings required by the app, if any
5. Update the database

The Snippets app is a good place to understand the procedure. Step 1::

    pip install git+https://code.eliotberriot.com/kii/kii-snippets.git

Step 2 and 3::

    nano kii_instance/settings.py


The INSTALLED_APPS part of settings should look like this::

    INSTALLED_APPS += (
        # insert kii apps here
        # ...
        "kii_snippets.apps.App",
    )

Step 4: add required markdown extension for code highlighting::

    from kii_snippets.settings import md_filter

    MARKUP_FIELD_TYPES += (
        ('markdown', md_filter),
    )

Step 5:

    python manage.py syncdb





