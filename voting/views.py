from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Vote, VoteCount
from django.contrib.auth.models import User


def reset_vote_counts():
    VoteCount.objects.all().delete()
    for user in User.objects.all():
        if not user.is_superuser:
            VoteCount(user=user, votes=0).save()
    for vote in VoteCount.objects.all():
        vote.update_count()


# Create your views here.
def index(request):
    reset_vote_counts()
    votes = Vote.objects.order_by('time')
    votecounts = [v.get_list() for v in VoteCount.objects.order_by('votes')]
    users = User.objects.all().filter(is_superuser=False)
    context = {
        'votes': votes,
        'votecounts': votecounts,
        'users': users,
    }
    return render(request, 'index.html', context=context)


def vote(request):
    voter = get_object_or_404(User, pk=request.user.pk)
    votee = User.objects.get(pk=request.POST['votee'])
    Vote(voter=voter, votee=votee).save()
