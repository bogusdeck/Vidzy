from django.db import models

class VideoUpload(models.Model):
    video = models.FileField(upload_to='videos/')
    subtitle = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.name
