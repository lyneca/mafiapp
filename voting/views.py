from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Vote, VoteCount
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime


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
    votecounts = [v.get_list() for v in VoteCount.objects.all().exclude(votes=0).order_by('votes').reverse()]
    users = User.objects.all().filter(is_superuser=False, is_active=True)
    context = {
        'time': datetime.datetime.now().time().isoformat().split(':')[0],
        'votes': votes,
        'votecounts': votecounts,
        'active_users': users,
        'user': request.user
    }
    return render(request, 'index.html', context=context)


def vote(request):
    voter = get_object_or_404(User, pk=request.user.pk)
    if Vote.objects.filter(voter=voter):
        for vote in Vote.objects.all().filter(voter=voter):
            vote.active = False
            vote.save()
    if not request.POST['votee'] == '-1':
        votee = User.objects.get(pk=request.POST['votee'])
        Vote(voter=voter, votee=votee).save()
    else:
        Vote(voter=voter, votee=voter, is_cancel=True).save()
    return HttpResponseRedirect(reverse('voting:index'))


def log_in(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
            login(request, user)
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        print("The username and password were incorrect.")
    return HttpResponseRedirect(reverse('voting:index'))


def change_pwd(request):
    newpwd = request.POST['newpwd']
    user = request.user
    request.user.set_password(newpwd)
    request.user.save()
    user = authenticate(username=user.username, password=newpwd)
    login(request, user)
    return HttpResponseRedirect(reverse('voting:index'))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('voting:index'))


def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        'user': user,
        'votes': Vote.objects.filter(voter=user),
        'voted': Vote.objects.filter(votee=user),
    }
    return render(request, 'user_profile.html', context=context)
