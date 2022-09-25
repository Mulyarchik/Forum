from django.shortcuts import render

from .models import Thread, Post, User

def backends(request):
    thread = Thread.objects.all()

