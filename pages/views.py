from django.shortcuts import render
from pages.models import Contact
from datetime import datetime
from django.contrib import messages
from blog.models import Post
from accounts.models import  UserProfile
from django.http import HttpResponseForbidden, Http404

def csrf_failure(request, reason=""):
    return render(request, '403.html', status=403)

def test_403(request):
    return HttpResponseForbidden("You don't have access.")

def test_404(request):
    raise Http404("Page not found")


def error_403(request, exception=None):
    return render(request, 'pages/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'pages/404.html', status=404)

def error_500(request):
    return render(request, 'pages/500.html', status=500)

def test_500(request):
    1 / 0  # type: ignore # triggers ZeroDivisionError 

# Create your views here.
def home(request):
    posts = Post.objects.filter(published=True).order_by('-created')
    authors = UserProfile.objects.select_related('user').all()[:10] 
    return render(request, 'pages/home.html', {'posts': posts, 'authors': authors})

def terms(request):
    return render(request, 'pages/terms.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, subject=subject, message=message, date = datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def help_page(request):
    return render(request, 'pages/help.html')