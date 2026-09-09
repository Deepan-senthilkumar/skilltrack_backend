from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    StudentRegisterView,
    MeView,
    StudentListView,
    StaffStudentCreateView,
    StaffStudentDeleteView,
    StaffFacultyListView,
    StaffFacultyCreateView,
    StaffFacultyDeleteView,
    AdminUserListCreateView,
    AdminUserDetailView,
)

urlpatterns = [
    # Auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/student-register/', StudentRegisterView.as_view(), name='student_register'),
    path('auth/me/', MeView.as_view(), name='me'),

    # Admin User Management
    path('admin/users/', AdminUserListCreateView.as_view(), name='admin-users-list-create'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-users-detail'),

    # Staff / Faculty
    path('staff/faculty/', StaffFacultyListView.as_view(), name='staff-faculty-list'),
    path('staff/faculty/create/', StaffFacultyCreateView.as_view(), name='staff-faculty-create'),
    path('staff/faculty/<int:pk>/', StaffFacultyDeleteView.as_view(), name='staff-faculty-delete'),

    # Students
    path('staff/students/', StudentListView.as_view(), name='staff-students-list'),
    path('staff/students/create/', StaffStudentCreateView.as_view(), name='staff-student-create'),
    path('staff/students/<int:pk>/', StaffStudentDeleteView.as_view(), name='staff-student-delete'),
]
