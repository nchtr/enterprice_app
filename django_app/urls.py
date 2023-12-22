from django.urls import path

from django_app import views


urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_, name="login")
    
]
