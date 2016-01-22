from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='voter')
    votee = models.ForeignKey(User, related_name='votee')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voter.get_full_name() + ' voted for ' + self.votee.get_full_name()
