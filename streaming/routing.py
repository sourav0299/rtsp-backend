from streaming.consumers import StreamConsumer
from django.urls import path

websocket_urlpatterns = [
    path("ws/stream/", StreamConsumer.as_asgi()),
]
