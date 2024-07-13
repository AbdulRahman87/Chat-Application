from django.shortcuts import render
from .models import Group, Chat
from django.core import serializers

# Create your views here.

def index(request, group_name):
    if group_name != 'favicon.ico':
        try:
            group = Group.objects.get(name=group_name)
        except Exception as e:
            group = Group(name=group_name)
            group.save()
    chats = Chat.objects.filter(group=group)
    chats = serializers.serialize("json", chats)
    return render(request, 'index.html', {'group_name': group_name, 'chats': chats})

def home(reqeust):
    groups = Group.objects.all()
    return render(reqeust, 'home.html', {'groups': groups})