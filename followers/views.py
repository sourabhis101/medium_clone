from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Follow

@login_required
def follow_user(request, user_id):
    target = get_object_or_404(CustomUser, id=user_id)
    if request.user != target:
        Follow.objects.get_or_create(follower=request.user, following=target)
    return redirect('dashboard')

@login_required
def unfollow_user(request, user_id):
    target = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.filter(follower=request.user, following=target).delete()
    return redirect('dashboard')
