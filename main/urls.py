from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]
