from .consumer import myAsyncConsumer
from django.urls import path

websocket_urlpatterns = [
    path("ws/ac/<str:groupname>/", myAsyncConsumer.as_asgi())
]