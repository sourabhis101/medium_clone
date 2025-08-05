from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    
    path('@<str:username>/<slug:slug>/', views.post_detail, name='post_detail'), # type: ignore
    path('@<str:username>/', views.author_profile, name='author_profile'),
    path('search/', views.search_posts, name='search'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('@<username>/<slug:slug>/comment/', views.add_comment, name='add_comment'), # type: ignore
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
]
