from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='voter')
    votee = models.ForeignKey(User, related_name='votee')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voter.get_full_name() + ' voted for ' + self.votee.get_full_name()


class VoteCount(models.Model):
    user = models.ForeignKey(User, related_name='user')
    votes = models.IntegerField(default=0)

    def update_count(self):
        vote_objects_for_me = Vote.objects.all().filter(votee=self.user)
        votes_for_me = vote_objects_for_me.count()
        self.votes = votes_for_me
        self.save()

    def get_list(self):
        return [self.user.get_full_name(), self.votes]

    def __str__(self):
        return self.user.get_full_name() + ': ' + str(self.votes)
