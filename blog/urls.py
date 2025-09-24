# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/update/<int:pk>/', views.post_update, name='post_update'),
    path('posts/delete/<int:pk>/', views.post_delete, name='post_delete'),  # <-- delete URL
    path('fetch-dogs/', views.fetch_external_posts, name='fetch_external_posts'),
    path('chart/', views.chart, name='chart'),
]
