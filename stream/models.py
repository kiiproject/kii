from django.db import models

class Stream(models.Model):
    pass
    
class StreamItem(models.Model):

    stream = models.ForeignKey(Stream, related_name="items")