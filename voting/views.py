from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Vote, VoteCount
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


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
    votes = Vote.objects.filter(
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
        )
    ).order_by('time')
    votecounts = [v.get_list() for v in VoteCount.objects.all().exclude(votes=0).order_by('votes').reverse()]
    users = User.objects.all().filter(is_superuser=False, is_active=True)
    if 21 > datetime.now().hour >= 6:
        can_vote = True
    else:
        can_vote = False
    context = {
        'time': datetime.now().time().isoformat().split(':')[0],
        'votes': votes,
        'votecounts': votecounts,
        'active_users': users,
        'user': request.user,
        'can_vote': can_vote,
    }
    return render(request, 'index.html', context=context)


def vote(request):
    voter = get_object_or_404(User, pk=request.user.pk)
    if Vote.objects.filter(voter=voter):
        for vote in Vote.objects.all().filter(voter=voter):
            vote.active = False
            vote.save()
    if 'votee' in request.POST:
        if not request.POST['votee'] == '-1':
            votee = User.objects.get(pk=request.POST['votee'])
            Vote(voter=voter, votee=votee).save()
        else:
            Vote(voter=voter, votee=voter, is_cancel=True).save()
            messages.success(request, "Vote recorded!")
    return HttpResponseRedirect(reverse('voting:index'))


def log_in(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
            messages.success(request, "You have been successfully logged in.")
            login(request, user)
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        print("The username or password was incorrect.")
        messages.success(request, "The username or password was incorrect.")
    return HttpResponseRedirect(reverse('voting:index'))


def change_pwd(request):
    newpwd = request.POST['newpwd']
    user = request.user
    request.user.set_password(newpwd)
    request.user.save()
    user = authenticate(username=user.username, password=newpwd)
    login(request, user)
    messages.success(request, "Your password has been changed.")
    return HttpResponseRedirect(reverse('voting:index'))


def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return HttpResponseRedirect(reverse('voting:index'))


def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        'user': user,
        'votes': Vote.objects.filter(voter=user),
        'voted': Vote.objects.filter(votee=user),
    }
    return render(request, 'user_profile.html', context=context)


def delete_vote(request):
    vote = Vote.objects.get(pk=request.POST['vote_id'])
    vote.delete()
    messages.success(request, "Vote deleted.")
    return HttpResponseRedirect(reverse('voting:index'))


def deactivate(request):
    user = User.objects.get(pk=request.POST['user'])
    user.is_active = False
    user.save()
    messages.success(request, "User killed.")
    return HttpResponseRedirect(reverse('voting:index'))
