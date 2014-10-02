from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

class UserData(models.Model):
    """Used to store additional data in user model, without extending or replaceing it"""
    pass
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="data")

def create_user_data(sender, instance, created, **kwargs):
    if created:
        ud = UserData(user=instance)
        ud.save()

post_save.connect(create_user_data, sender=settings.AUTH_USER_MODEL)