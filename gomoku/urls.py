from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/gomoku/', consumers.GomokuConsumer.as_asgi())
]