# myblog/urls.py

from django.urls import path, re_path
# from .views import post_list, post_detail, post_create, root_view
from .views import (
    post_list, post_detail, post_create, post_update, post_delete,
    category_list, category_create, category_update, category_delete,
    tag_list, tag_create, tag_update, tag_delete,
    comment_delete, root_view, comment_create
)
from .consumers import CommentConsumer

# app_name = 'myblog'
urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('', root_view, name='root'),
]

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:pk>/update/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    
    path('category/', category_list, name='category_list'),
    path('category/create/', category_create, name='category_create'),
    path('category/<int:pk>/update/', category_update, name='category_update'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),
    
    path('tag/', tag_list, name='tag_list'),
    path('tag/create/', tag_create, name='tag_create'),
    path('tag/<int:pk>/update/', tag_update, name='tag_update'),
    path('tag/<int:pk>/delete/', tag_delete, name='tag_delete'),

    path('comment/create/<int:post_pk>/', comment_create, name='comment_create'),
    # path('comment/create/<int:pk>/', comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),

    path('post/<int:pk>/delete/', post_delete, name='post_delete'),

    re_path(r'ws/comment/(?P<post_pk>\d+)/$', CommentConsumer.as_asgi()),
]