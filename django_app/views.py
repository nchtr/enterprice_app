import datetime
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.cache import caches
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from django_app import models, serializers
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

# Create your views here.

RamCache = caches["default"]
DatabaseCache = caches["extra"]


def register(request):
    if request.method == "GET":
        return render(request, "registerpage.html")
    elif request.method == "POST":
        email = str(request.POST.get("email", None)).strip()  # Admin1@gmail.com
        password = str(request.POST.get("password", None)).strip()  # Admin1@gmail.com
        valid_email = re.match(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", email)
        valid_password = re.match(
            r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!.]).*$", password
        )

        # print(f"valid_email: ", valid_email)
        # print(f"valid_password: ", valid_password)

        if valid_email is None or valid_password is None:
            return render(
                request,
                "registerpage.html",
                {"error": "Некорректный формат email или пароль"},
            )
        try:
            user = User.objects.create(
                username=email,
                password=make_password(password),  # HASHING PASSWORD
                email=email,
            )

        except Exception as error:
            return render(
                request,
                "registerpage.html",
                {"error": str(error)},
            )
        return redirect(reverse("login"))
    else:
        raise ValueError("Invalid method")


def login_(request: HttpRequest) -> HttpResponse:
    """Вход в аккаунт пользователя."""

    if request.method == "GET":
        return render(request, "loginpage.html")
    elif request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is None:
            return render(
                request, "loginpage.html", {"error": "Некорректный email или пароль"}
            )
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")


@login_required
def logout_(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта"""

    logout(request)
    return redirect(reverse("home"))


class HomePage(View):
    def get(self, request):
        news = self.get_news()
        return render(
            request=request,
            template_name="mainpage.html",
            context={"first": news[0], "second": news[1], "third": news[2]},
        )

    def get_news(self):
        data = RamCache.get(f"news")
        if data is None:
            data = []
            news_api = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=21ae35ce91a5473e8a0a9ce12c03db7d"
            for i in requests.get(news_api).json()["articles"]:
                data.append(
                    {
                        "author": i["author"],
                        "title": i["title"],
                        "publish_date": datetime.datetime.strftime(
                            datetime.datetime.fromisoformat(str(i["publishedAt"])),
                            "%d.%m.%Y",
                        ),
                        "publish_time": datetime.datetime.strftime(
                            datetime.datetime.fromisoformat(str(i["publishedAt"])),
                            "%H:%M",
                        ),
                        "url": i["url"],
                    }
                )
            RamCache.set(f"news", data, timeout=480)

        return data


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def js_debug_page(request) -> Response:
    user = models.User.objects.get(username=request.user.username)
    userdata = serializers.UserSerializer(user, many=False).data
    return Response(data=userdata, status=status.HTTP_200_OK)


@login_required
def room(request, slug):
    room_obj = models.Room.objects.get(slug__chat_slug=slug)
    print(room_obj)
    messages = models.Message.objects.filter(room=room_obj)[:2][::-1]
    return render(
        request, "chat_room.html", context={"room": room_obj, "messages": messages}
    )


@login_required
def vacancies_list(request):
    vacancieslist = models.Vacancies.objects.all()
    return render(
        request=request,
        template_name="vacanciespage.html",
        context={"vacancies": vacancieslist},
    )


@login_required
def vacancy_detail(request, slug):
    vacancy = models.Vacancies.objects.get(slug=slug)
    return render(request, "vacancydetail.html", context={"vacancy": vacancy})


@login_required
def resume_request(request):
    if request.method == "GET":
        return render(request, "resumeform.html", context={"success": "True"})
    elif request.method == "POST":
        if models.Resume.objects.filter(person__username=request.user).count() < 1:
            models.Resume.objects.create(
                person=request.user,
                title=str(request.POST["title"]),
                first_name=str(request.POST["first_name"]),
                last_name=str(request.POST["last_name"]),
                iin=request.POST["iin"],
                text=str(request.POST["text"]),
                photo=request.FILES.get("photo", None),
                documents=request.FILES.get("file", None),
            )
            return redirect(reverse("resumerequest"))

        else:
            return redirect(reverse("resumerequest"))


@login_required
def vac_response(request, slug):
    vac = models.Vacancies.objects.get(slug=slug)
    res = models.Resume.objects.get(person=request.user)
    models.VacancyRequests.objects.create(title=vac, resume=res)
    return redirect(reverse("vacancies"))


@login_required
def post_list(request):
    posts = models.Post.objects.filter(is_active=True)
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(posts, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(
        request,
        "postpage.html",
        context={"current_page": current_page, "is_detail_view": True},
    )


@login_required
def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    # 1. Проверяем, нет ли объект-а в кэш-е
    # 1.1 Если есть, возвращаем кэш
    # 2. Получаем объект из базы данных
    # 2.1 Кэшируем объект
    # 2.2 Возращаем объект

    post = RamCache.get(f"post_detail_{slug}")
    if post is None:
        post = models.Post.objects.get(
            slug=slug
        )  # тяжёлое обращение к базе данных -- 100x - 1000x
        RamCache.set(f"post_detail_{slug}", post, timeout=30)

    # Если мы поставили лайк - то закрашиваем кнопку
    # post + user

    comments = models.PostComments.objects.filter(post=post)
    ratings = models.PostRatings.objects.filter(post=post)
    ratings = {
        "like": ratings.filter(status=True).count(),
        "dislike": ratings.filter(status=False).count(),
        "total": ratings.filter(status=True).count()
        - ratings.filter(status=False).count(),
    }

    return render(
        request,
        "postdetail.html",
        context={
            "post": post,
            "comments": comments,
            "ratings": ratings,
            "is_detail_view": True,
        },
    )


@login_required
def post_post(request):
    if request.method == "GET":
        return render(request, "postform.html")
    elif request.method == "POST":
        models.Post.objects.create(
            author=request.user,
            title=request.POST["title"],
            description=request.POST["description"],
            image=request.FILES.get("image", None),
        )
        return redirect(reverse("postlist"))


@login_required
def post_list_simple(request: HttpRequest) -> HttpResponse:
    posts = models.Post.objects.filter(is_active=True)
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(posts, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(
        request,
        "postpage.html",
        context={"current_page": current_page, "is_detail_view": False},
    )


@login_required
def post_comment(request, slug):
    post = models.Post.objects.get(slug=slug)
    text = request.POST.get("text", "")
    models.PostComments.objects.create(post=post, author=request.user, text=text)

    return redirect(reverse("post_detail", args=(slug,)))


@login_required
def post_rating(request: HttpRequest, slug, is_like: str) -> HttpResponse:
    post = models.Post.objects.get(slug=slug)
    is_like = (
        True if str(is_like).lower().strip() == "лайк" else False
    )  # тернарный оператор

    ratings = models.PostRatings.objects.filter(post=post, author=request.user)
    if len(ratings) < 1:
        models.PostRatings.objects.create(
            post=post, author=request.user, status=is_like
        )
    else:
        rating = ratings[0]
        if is_like is True and rating.status is True:
            rating.delete()
        elif is_like is False and rating.status is False:
            rating.delete()
        else:
            rating.status = is_like
            rating.save()

    return redirect(reverse("postdetail", args=(slug,)))


@login_required
def post_hide(request: HttpRequest, slug: str) -> HttpResponse:
    post = models.Post.objects.get(slug=slug)
    post.is_active = False
    post.save()
    return redirect(reverse("postlist"))


@login_required
def post_comment_create(request: HttpRequest, slug: str) -> HttpResponse:
    """Создание комментария."""

    post = models.Post.objects.get(slug=slug)
    text = request.POST.get("text", "")
    models.PostComments.objects.create(post=post, author=request.user, text=text)

    return redirect(reverse("postdetail", args=(slug,)))


def profile(request):
    return render(request=request, template_name="build/index.html")
