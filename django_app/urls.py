from django.urls import path

from django_app import views
from django_app import aviews

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_, name="login"),
    path("logout/", views.logout_, name="logout"),
    path("messages/", views.messages),
    path("<slug:slug>/", views.room, name="room"),
    path("vacancies", views.vacancies_list, name="vacancies"),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

websocket_urlpatterns = [
    path('ws/<slug:room_name>/', aviews.ChatConsumer.as_asgi())
]