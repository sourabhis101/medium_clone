

# Create your views here.
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from django.core.exceptions import SuspiciousOperation

def trigger_400(request):
    raise SuspiciousOperation("Bad request triggered for testing")



def trigger_403(request):
    raise PermissionDenied

def home(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def help_page(request):
    return render(request, 'pages/help.html')

def about(request):
    return render(request, 'pages/about.html')

def terms(request):
    return render(request, 'pages/terms.html')

def custom_400_view(request, exception):
    return render(request, 'pages/400.html', status=400)

def custom_403_view(request, exception):
    return render(request, 'pages/403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)

def custom_500_view(request):
    return render(request, 'pages/500.html', status=500)

def trigger_500(request):
    1 / 0   # type: ignore
