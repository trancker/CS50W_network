
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("writepost",views.writepost,name="writepost"),
    path("submitpost",views.submitpost,name="submitpost"),
    path("postapi/<int:postid>",views.postapi,name="postapi"),
    path("profile/<str:uname>",views.profilepage,name="profilepage"),
    path("followapi/<str:name>",views.followapi,name="followapi"),
    path("follow/<str:name>",views.followuser,name="followuser"),
    path("unfollow/<str:name>",views.unfollowuser,name="unfollowuser"),
    path("followingposts",views.followingposts,name="followingposts"),
    path("likesapi/<int:postid>",views.likesapi,name="likesapi")
]
