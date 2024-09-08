import os
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from .models import VideoUpload
from django.conf import settings
import subprocess

# def handle_uploaded_video(video_path):
#     subtitle_path = os.path.splitext(video_path)[0] + '.srt'
#     # Run CCExtractor to extract subtitles
#     subprocess.run(['ccextractor', video_path, '-o', subtitle_path])
#     # Read the subtitle file content
#     if os.path.exists(subtitle_path):
#         with open(subtitle_path, 'r') as subtitle_file:
#             subtitles = subtitle_file.read()
#         return subtitles
#     else:
#         return "No subtitles found."

def handle_uploaded_video(video_path):
    subtitle_path = os.path.splitext(video_path)[0] + '.srt'

    # Use additional options for CCExtractor to increase compatibility
    command = [
        'ccextractor',
        video_path,
        '-o', subtitle_path,  # Output subtitle file
        '--autoprogram',      # Automatic selection of subtitle stream
        '--utf8',             # Output in UTF-8 encoding
        '--no_font_color',    # Remove color info for better compatibility
    ]

    subprocess.run(command)
    
    # Check if subtitle file was created and has content
    if os.path.exists(subtitle_path) and os.path.getsize(subtitle_path) > 0:
        with open(subtitle_path, 'r') as subtitle_file:
            subtitles = subtitle_file.read()
        return subtitles
    else:
        return "No subtitles found or could not extract subtitles."


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
    video = get_object_or_404(VideoUpload, id=video_id)
    return render(request, 'video/detail.html', {'video': video})


def index(request):
    return render("index.html")