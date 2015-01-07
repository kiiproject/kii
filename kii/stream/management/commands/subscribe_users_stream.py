from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from actstream.actions import follow
from actstream import registry

from kii.stream.models import Stream

class Command(BaseCommand):
    help =  """Subscribe legacy users to their stream activity. It is done
    automatically for newly created users"""

    def handle(self, *args, **options):

        registry.register(Stream)

        for user in get_user_model().objects.all():

            stream = Stream.objects.get(title=user.username, owner=user)        
            follow(user, stream, actor_only=False)
            self.stdout.write('Subscribed user {0} to stream {1}'.format(user, stream))
