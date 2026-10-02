from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add/', views.add_student, name='add_student'),
    path('admin-dashboard/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('admin-dashboard/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('admin-dashboard/view/<int:pk>/', views.view_student, name='view_student'),
]
