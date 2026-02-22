from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/upload-csv/', views.admin_upload_csv, name='admin_upload_csv'),
    path('admin-dashboard/manual-entry/', views.admin_manual_entry, name='admin_manual_entry'),
    path('admin-dashboard/performance/', views.admin_performance, name='admin_performance'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]
