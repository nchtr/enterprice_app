import datetime
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import requests

# Create your views here.

def register(request):
        if request.method == "GET":
            return render(request, "registerpage.html")
        elif request.method == "POST":
            email = str(request.POST.get("email", None)).strip()  # Admin1@gmail.com
            password = str(request.POST.get("password", None)).strip()  # Admin1@gmail.com
            valid_email = re.match(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", email)
            valid_password = re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!.]).*$", password)

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
            return render(request, "loginpage.html", {"error": "Некорректный email или пароль"})
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")

class HomePage(View):
    def get(self, request):
        news = self.get_news()
        return render(request=request, template_name="mainpage.html", )
    
    def get_news(self):
        data=[]
        news_api="https://newsapi.org/v2/top-headlines?country=ru&apiKey=21ae35ce91a5473e8a0a9ce12c03db7d"
        for i in requests.get(news_api).json()["articles"]:
            data.append({'author':i["author"], 'title':i['title'], 'publish_date':datetime.datetime.strftime(datetime.datetime.fromisoformat(str(i['publishedAt'])), '%d.%m.%Y'), 'publish_time':datetime.datetime.strftime(datetime.datetime.fromisoformat(str(i['publishedAt'])), '%H:%M'), 'url':i['url']})
        return data
    
    def login_from_main(self, request):
        if request.method == "GET":
            return render(request, "mainpage.html")
        elif request.method == "POST":
            email = request.POST.get("email", None)
            password = request.POST.get("password", None)
            user = authenticate(request, username=email, password=password)
            if user is None:
                return render(request, "loginpage.html", {"error": "Некорректный email или пароль"})
            login(request, user)
            return redirect(reverse("home"))
        else:
            raise ValueError("Invalid method")