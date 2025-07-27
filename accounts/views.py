from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate  , login , logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm , LoginForm
from .forms import UserProfileForm

from django.views.decorators.csrf import csrf_protect



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')




@login_required
def edit_profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('author_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


def signupview(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have registered your account.")
            return redirect('login')  # ✅ return must be inside this block
        else:
            print("Form errors:", form.errors)  
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    # ✅ return after both POST and GET cases
    return render(request, 'accounts/signup.html', {'form': form})
        
@csrf_protect        
def loginview(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)      
                return redirect('/')
            else:
                form = LoginForm()
                messages.error(request, "Invalid username or password")  # ✅
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html',{'form': form})


        
def forgetpassword(request):
    return render(request, 'accounts/forget-password.html')
def password_reset_key(request):
    return render(request, 'accounts/password-reset-key.html')
def password_reset_key_done(request):
    return render(request, 'accounts/password-reset-key-done.html')


