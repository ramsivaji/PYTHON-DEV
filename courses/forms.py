from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Subject, Video

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Subject Description (optional)'}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['subject', 'number', 'title', 'description', 'drive_link']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Video Description (optional)'}),
            'drive_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Google Drive View or Embed Link'}),
        }
