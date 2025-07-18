from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import EmailAuthenticationForm # use the custom form
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import UserCreationForm

User = get_user_model()
# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.save()
            
            user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login View

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'accounts/logout.html')

# Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

# Password Reset Request
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            users = User.objects.filter(email=user_email)
            for user in users:
                subject = "Password Reset Request"
                email_template = render_to_string('accounts/email.html', {
                    'email': user.email,
                    'domain': request.get_host(),
                    'site_name': 'Medium_clone',
                    'uid': user.pk,
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                })
                send_mail(subject, email_template, settings.DEFAULT_FROM_EMAIL, [user.email])
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

# Password Reset Done
def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

# Password Reset Confirm
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_from_key.html', {'form': form})
    else:
        return render(request, 'accounts/password_reset_from_key_invalid.html')

# Email Confirm Placeholder (you can connect it later with allauth if needed)
def email_confirm_view(request):
    return render(request, 'accounts/email_confirm.html')
