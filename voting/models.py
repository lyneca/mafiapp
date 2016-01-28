from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='voter')
    votee = models.ForeignKey(User, related_name='votee')
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    is_cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.voter.get_full_name() + ' voted for ' + self.votee.get_full_name()


class VoteCount(models.Model):
    user = models.ForeignKey(User, related_name='user')
    votes = models.IntegerField(default=0)

    def update_count(self):
        vote_objects_for_me = Vote.objects.all().filter(
                votee=self.user, active=True, is_cancel=False,
                time__range=(
                    datetime(
                            datetime.now().year,
                            datetime.now().month,
                            datetime.now().day,
                            6, 0, 0, 0
                    ),
                    datetime(
                            datetime.now().year,
                            datetime.now().month,
                            datetime.now().day,
                            21, 0, 0, 0
                    )
                ))
        votes_for_me = vote_objects_for_me.count()
        self.votes = votes_for_me
        self.save()

    def get_list(self):
        return [self.user, self.votes]

    def __str__(self):
        return self.user.get_full_name() + ': ' + str(self.votes)


""""
> Luke Tuthill voted for Craig Smith
> Zac Francis voted for Jarvis Carroll
> Craig Smith voted for Luke Tuthill
> Sam Kelly voted for Craig Smith
"""
