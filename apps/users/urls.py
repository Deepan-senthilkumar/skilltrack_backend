from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, StudentRegisterView, CustomTokenObtainPairView,
    MeView, StudentListView,
    StaffStudentCreateView, StaffStudentDeleteView,
    StaffFacultyListView, StaffFacultyCreateView, StaffFacultyDeleteView
)

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/student-register/', StudentRegisterView.as_view(), name='student-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),

    # Student Roster
    path('staff/students/', StudentListView.as_view(), name='staff-students-list'),
    path('staff/students/create/', StaffStudentCreateView.as_view(), name='staff-students-create'),
    path('staff/students/<int:pk>/', StaffStudentDeleteView.as_view(), name='staff-students-delete'),

    # Faculty & Staff Team Management (Admin)
    path('staff/faculty/', StaffFacultyListView.as_view(), name='staff-faculty-list'),
    path('staff/faculty/create/', StaffFacultyCreateView.as_view(), name='staff-faculty-create'),
    path('staff/faculty/<int:pk>/', StaffFacultyDeleteView.as_view(), name='staff-faculty-delete'),
]
