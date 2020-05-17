from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.myprofile, name="myprofile"),
    path("<int:user_id>", views.profile, name="profile"),   
    path("<int:user_id>/accept", views.accept, name="accept"),


]
