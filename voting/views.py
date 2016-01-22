from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Vote, VoteCount
from django.contrib.auth import authenticate, login, logout
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
    votecounts = [v.get_list() for v in VoteCount.objects.order_by('votes').reverse()]
    users = User.objects.all().filter(is_superuser=False)
    context = {
        'votes': votes,
        'votecounts': votecounts,
        'users': users,
        'user': request.user
    }
    return render(request, 'index.html', context=context)


def vote(request):
    voter = get_object_or_404(User, pk=request.user.pk)
    votee = User.objects.get(pk=request.POST['votee'])
    Vote.objects.get(voter=voter).delete()
    Vote(voter=voter, votee=votee).save()
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
