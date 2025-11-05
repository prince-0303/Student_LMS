from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/edit-profile/', views.edit_profile, name='edit_profile'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add/', views.add_student, name='add_student'),
    path('admin-dashboard/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('admin-dashboard/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('admin-dashboard/block/<int:student_id>/', views.block_student, name='block_student'),
    path('admin-dashboard/unblock/<int:student_id>/', views.unblock_student, name='unblock_student'),

]
