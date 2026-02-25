from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    number = models.IntegerField(help_text="Video ordering number")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    drive_link = models.URLField(help_text="Google Drive embed or view link")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}. {self.title}"
