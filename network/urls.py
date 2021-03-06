
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('post/create', views.create_post, name='create_post'),
    path('like', views.like_post, name='like_post'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('following_page', views.following_page, name='following_page')
]
