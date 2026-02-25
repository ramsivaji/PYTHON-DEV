from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Subject, Video
from .forms import AdminLoginForm, SubjectForm, VideoForm

# --- VIEWER PANEL (Public) --- #

def home_view(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'courses/viewer/home.html', {'subjects': subjects})

def subject_detail_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    videos_list = subject.videos.all().order_by('number')
    
    # Pagination
    paginator = Paginator(videos_list, 10) # 10 videos per page
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)
    
    return render(request, 'courses/viewer/subject_detail.html', {
        'subject': subject,
        'videos': videos
    })

def video_play_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Extract Google Drive ID from link if possible to embed easily
    # Usually links are: https://drive.google.com/file/d/VIDEO_ID/view...
    drive_link = video.drive_link
    embed_link = drive_link
    if '/view' in drive_link and '/d/' in drive_link:
        try:
            video_hash = drive_link.split('/d/')[1].split('/')[0]
            embed_link = f"https://drive.google.com/file/d/{video_hash}/preview"
        except IndexError:
            pass
            
    return render(request, 'courses/viewer/video_play.html', {
        'video': video,
        'embed_link': embed_link
    })


# --- ADMIN PANEL --- #

def admin_login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AdminLoginForm()
    
    return render(request, 'courses/admin_panel/login.html', {'form': form})

@login_required(login_url='admin_login')
def admin_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_dashboard_view(request):
    subject_count = Subject.objects.count()
    video_count = Video.objects.count()
    recent_videos = Video.objects.order_by('-created_at')[:5]
    return render(request, 'courses/admin_panel/dashboard.html', {
        'subject_count': subject_count,
        'video_count': video_count,
        'recent_videos': recent_videos
    })

# Subject CRUD
@login_required(login_url='admin_login')
def subject_list_view(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'courses/admin_panel/subject_list.html', {'subjects': subjects})

@login_required(login_url='admin_login')
def subject_create_view(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created successfully.")
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'courses/admin_panel/subject_form.html', {'form': form, 'title': 'Create Subject'})

@login_required(login_url='admin_login')
def subject_update_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'courses/admin_panel/subject_form.html', {'form': form, 'title': 'Edit Subject'})

@login_required(login_url='admin_login')
def subject_delete_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect('subject_list')
    return render(request, 'courses/admin_panel/subject_confirm_delete.html', {'subject': subject})

# Video CRUD
@login_required(login_url='admin_login')
def video_list_view(request):
    videos_list = Video.objects.all().order_by('subject__name', 'number')
    paginator = Paginator(videos_list, 15)
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)
    return render(request, 'courses/admin_panel/video_list.html', {'videos': videos})

@login_required(login_url='admin_login')
def video_create_view(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Video added successfully.")
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'courses/admin_panel/video_form.html', {'form': form, 'title': 'Add Video'})

@login_required(login_url='admin_login')
def video_update_view(request, pk):
    video = get_object_or_440(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully.")
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'courses/admin_panel/video_form.html', {'form': form, 'title': 'Edit Video'})

@login_required(login_url='admin_login')
def video_delete_view(request, pk):
    video = get_object_or_440(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully.")
        return redirect('video_list')
    return render(request, 'courses/admin_panel/video_confirm_delete.html', {'video': video})
