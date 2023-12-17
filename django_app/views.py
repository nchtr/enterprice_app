from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "mainpage.html")
    # return JsonResponse({"status": "OK"}, safe=True)

