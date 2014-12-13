Warning
#######

Kii is still in early development. Do not use it unless you're ready to experience breaks in API, bugs, universe collapsing, etc.


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

    source ./kii-virtualenv/bin/activate

Then install required packages (PyPi install will be available soon)::

    pip install kii

Now, you can create a new kii instance using a template::

    django-admin.py startproject kii_instance --template=https://code.eliotberriot.com/kii/kii-instance-template/repository/archive.zip --extension=py,sh

    cd kii_instance

It should create a kii_instance directory, with almost everything set up to make put your new kii instance online.

You can now adapt the settings under `kii_instance/settings.py` to suit your needs. For exemple, you will need to set your database credentials, your installed apps, etc. The settings file is heavily commented so I won't detail everything here.

When you're done, you can initialize the database with::

    python manage.py syncdb

    # create an admin account
    python manage.py createsuperuser

And collect static files::

    sudo mkdir /var/www/kii/static -p
    sudo chown kii:www-data /var/www/kii/static -R
    sudo chmod 770 /var/www/kii/static

    python manage.py collectstatic


Server deployment
#################

Nginx is the recommanded web server for deploying Kii, however, you can totally use Kii behind Apache2.

The following setup uses Supervisor and Gunicorn for easier maintenance of kii.

First, install dependencies::

    pip install gunicorn
    sudo apt-get install supervisor nginx

Then, check gunicorn is correctly working. You will have to make change to this file if you did not followed exactly the install procedure (different username, path, etc.):

    chmod +x ./gunicorn_start.sh
    ./gunicorn_start.sh

If Gunicorn works, you can now set up Nginx:

    sudo cp kii_instance/conf/nginx.conf /etc/nginx/sites-enabled/kii

    # Especially, in Nginx conf, you will have to set a correct server name.
    sudo nano /etc/nginx/sites-enabled/kii
    
    sudo service nginx reload

For easier management of your kii instance, you'll probably want to use a process manager. Your kii instance is bundled with a sample supervisor file you can use to start and stop your instance. Also, your instance will be started on boot, which is nice::

    sudo cp kii_instance/conf/supervisor.conf /etc/supervisor/conf.d/kii.conf

    # you can edit it, eventually, but defaults should be fine
    sudo nano /etc/supervisor/conf.d/kii.conf

    # launch the server
    sudo supervisorctl update
    sudo supervisorctl start kii

Install kii apps
################

As Kii is not bundled with any app, you app to install these separately. Each app may have custom installation instruction, but most of the process will remain identical:

1. Download the app python packages (via `pip install`)
2. Open `kii_instance/settings.py`
3. Add the app name under `INSTALLED_APPS`
4. (optional) in the same file, add custom settings required by the app, if any
5. Update the database

The Snippets app is a good place to understand the procedure. Step 1::

    pip install kii_snippets

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





