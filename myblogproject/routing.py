# myblog/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from .consumers import PostConsumer
from myblog.consumers import CommentConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'ws/comment/(?P<post_pk>\d+)/$', CommentConsumer.as_asgi()),
                path("ws/comment/<int:post_pk>/", CommentConsumer.as_asgi()),
                path("ws/post/", PostConsumer.as_asgi()),
            ]
        )
    ),
})
