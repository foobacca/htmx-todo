from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<html><body>Started the todo app</body></html>")
