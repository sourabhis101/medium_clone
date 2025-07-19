"""
URL configuration for medium_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from accounts.views import dashboard_view
from django.conf import settings
from django.conf.urls.static import static


# Error handlers
handler400 = 'pages.views.custom_400_view'
handler403 = 'pages.views.custom_403_view'
handler404 = 'pages.views.custom_404_view'
handler500 = 'pages.views.custom_500_view'



urlpatterns = [

    path('admin/', admin.site.urls),
         # ✅ auth   
    path('accounts/', include('accounts.urls')),  
    path('accounts/', include('allauth.urls')), 
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', include('blog.urls')),
    path('followers/', include('followers.urls')),
    path('', include('pages.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

