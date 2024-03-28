from django.urls import path
from .views import find_videos, find_pexels, find_mixkit, find_pixabay, index

urlpatterns = [
    path('find_videos', find_videos),
    path('find_pixabay', find_pixabay),
    path('find_mixkit', find_mixkit),
    path('find_pexels', find_pexels),
    path('', index)
]