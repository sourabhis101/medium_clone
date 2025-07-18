from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_page, name='help'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('trigger500/', views.trigger_500), # type: ignore
    path('trigger403/', views.trigger_403),
    path('trigger400/', views.trigger_400),

]
