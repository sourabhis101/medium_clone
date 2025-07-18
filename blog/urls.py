from django.urls import path
from . import views
from .views import upload_image , delete_image


urlpatterns = [
    path('post_list', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('search/',views.search_posts, name='search'), # type: ignore
     path('upload/image/', upload_image, name='upload_image'),
     path('delete/image/', delete_image, name='delete_image'),
]
