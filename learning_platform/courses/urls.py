from django.urls import path
from . import views

urlpatterns = [
    # Viewer URLs (Public)
    path('', views.home_view, name='home'),
    path('subject/<int:subject_id>/', views.subject_detail_view, name='subject_detail'),
    path('video/<int:video_id>/', views.video_play_view, name='video_play'),

    # Admin Auth
    path('admin-panel/login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),
    
    # Admin Dashboard
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Admin Subject CRUD
    path('admin-panel/subjects/', views.subject_list_view, name='subject_list'),
    path('admin-panel/subjects/create/', views.subject_create_view, name='subject_create'),
    path('admin-panel/subjects/<int:pk>/edit/', views.subject_update_view, name='subject_update'),
    path('admin-panel/subjects/<int:pk>/delete/', views.subject_delete_view, name='subject_delete'),

    # Admin Video CRUD
    path('admin-panel/videos/', views.video_list_view, name='video_list'),
    path('admin-panel/videos/create/', views.video_create_view, name='video_create'),
    path('admin-panel/videos/<int:pk>/edit/', views.video_update_view, name='video_update'),
    path('admin-panel/videos/<int:pk>/delete/', views.video_delete_view, name='video_delete'),
]
