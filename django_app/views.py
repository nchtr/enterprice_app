import datetime
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.cache import caches
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_app import models, serializers
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
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
        news1 = news
        post = self.get_mp_posts(request)
        print(post)
        return render(
            request=request,
            template_name="mainpage.html",
            context={
                "first": news1[0],
                "second": news1[1],
                "third": news1[2],
                "post": self.get_mp_posts(request),
            },
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

    def get_mp_posts(self, request):
        mp_post_ft = models.PostRatings.objects.order_by("-count")[:1]
        print(mp_post_ft)
        return mp_post_ft


@api_view(http_method_names=["GET", "POST"])  # красивый интерфейс
def messages(request: Request) -> Response:
    if request.method == "GET":
        message_list = models.Messages.objects.filter(
            from_user__username="admin"
        ) | models.Messages.objects.filter(to_user__username="admin")
        data = serializers.MessageSerializer(message_list, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        # {"message": "Привет Айгерим!"}
        print(request.GET)
        print(request.POST)
        print(request.FILES)
        # print(request.body)
        print(request.data)  # dictionary

        message: str = request.data.get("message", "")
        with open("messages.txt", "a", encoding="utf-8") as file:
            file.write(f"{message}\n")

        return Response(data={"message": "OK"}, status=status.HTTP_201_CREATED)


@login_required
def room(request, slug):
    room_obj = models.Room.objects.get(slug__chat_slug=slug)
    print(room_obj)
    messages = models.Message.objects.filter(room=room_obj)[:2][::-1]
    return render(
        request,
        "chat_room.html",
        context={"room": room_obj, "messages": messages}
    )
    
@login_required
def vacancies_list(request):
    vacancieslist=models.Vacancies.objects.all()
    print(vacancieslist)
    return render(request=request, template_name="vacanciespage.html", context={"vacancies":vacancieslist})