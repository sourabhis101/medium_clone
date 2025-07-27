from django.urls import path
from . import views

urlpatterns = [
        path('contact/', views.contact, name='contact'),
        path('terms/', views.terms, name='terms'),
        path('', views.home, name='home'),
        path('about/', views.about, name='about'),
        path('help/', views.help_page, name='help'),
        
    ]
