from django.contrib import admin
from .models import Subject, Video

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'subject', 'created_at')
    list_filter = ('subject',)
    search_fields = ('title', 'description')
    ordering = ('subject', 'number')
