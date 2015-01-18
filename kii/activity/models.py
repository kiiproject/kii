from django.db import models
from django.conf import settings
from actstream import models as actstream_models


class Notification(models.Model):
    """Inspirated from https://github.com/django-notifications/django-notifications/blob/master/notifications/models.py

    """

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications")
    action = models.ForeignKey(actstream_models.Action, related_name="notifications")
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-action__timestamp']

from django.db.models.signals import post_save

def send_notification(sender, instance, created, **kwargs):

    if not created:
        return

    recipients = actstream_models.followers(instance.actor)

    if instance.action_object:
        recipients += actstream_models.followers(instance.action_object)

    if instance.target:
        recipients += actstream_models.followers(instance.target)

    unique_recipients = set(recipients)
    for recipient in unique_recipients:
        n = Notification(recipient=recipient, action=instance)
        n.save()

post_save.connect(send_notification, sender=actstream_models.Action)



