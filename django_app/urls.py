from django.urls import path

from django_app import views
from django_app import aviews

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_, name="login"),
    path("logout/", views.logout_, name="logout"),
    path("api/debug/", views.js_debug_page),
    path("chat/<slug:slug>/", views.room, name="room"),
    path("vacancies", views.vacancies_list, name="vacancies"),
    path("vacancy/<slug:slug>/", views.vacancy_detail, name="vacancy"),
    path("resume/", views.resume_request, name="resumerequest"),
    path("vacancyresponse/<slug:slug>", views.vac_response, name="vacresponse"),
    path("posts/", views.post_list, name="postlist"),
    path("posts/simple/", views.post_list_simple, name="post_list_simple"),
    path("postdetail/<slug:slug>", views.post_detail, name="postdetail"),
    path("post/", views.post_post, name="postpost"),
    path("post/hide/<slug:slug>/", views.post_hide, name="post_hide"),
    path(
        "post/rating/<slug:slug>/<str:is_like>/", views.post_rating, name="post_rating"
    ),
    path(
        "post/comment/create/<slug:slug>/",
        views.post_comment_create,
        name="post_comment_create",
    ),
    path("profile/", views.profile, name="profile"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

websocket_urlpatterns = [path("ws/<slug:room_name>/", aviews.ChatConsumer.as_asgi())]
