from django.urls import path
from . import views
from .views import logout_view



urlpatterns = [
        path('signup/', views.signupview, name='signup'), 
        path('login/', views.loginview, name='login'),
        path('forget-password/', views.forgetpassword, name='forget-password'),
        path('password-reset-key/', views.password_reset_key, name='password-reset-key'),
        path('password-reset-key-done/', views.password_reset_key_done, name='password-reset-key-done'),
        path('edit-profile/', views.edit_profile, name='edit_profile'),
        path('logout/', logout_view, name='logout'), # type: ignore
        
         ]
