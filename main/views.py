import os
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import VideoUpload
from django.conf import settings
import subprocess

def handle_uploaded_video(video_path):
    subtitle_path = os.path.splitext(video_path)[0] + '.srt'
    # Run CCExtractor to extract subtitles
    subprocess.run(['ccextractor', video_path, '-o', subtitle_path])
    # Read the subtitle file content
    with open(subtitle_path, 'r') as subtitle_file:
        subtitles = subtitle_file.read()
    return subtitles

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save()
            video_path = os.path.join(settings.MEDIA_ROOT, video_instance.video.name)
            subtitles = handle_uploaded_video(video_path)
            video_instance.subtitle = subtitles
            video_instance.save()
            return redirect('video_detail', video_id=video_instance.id)
    else:
        form = VideoUploadForm()
    return render(request, 'video/upload.html', {'form': form})

def video_detail(request, video_id):
    video = VideoUpload.objects.get(id=video_id)
    return render(request, 'video/detail.html', {'video': video})
