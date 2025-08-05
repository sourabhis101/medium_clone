from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Follow

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        Follow.objects.get_or_create(follower=request.user, following=target_user)
    return redirect('author_profile', username=target_user.username)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('author_profile', username=target_user.username)
