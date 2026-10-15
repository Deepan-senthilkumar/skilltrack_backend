from django.urls import path
from controllers.super_admin import (
    SuperAdminLoginController,
    SuperAdminProfileController,
    SuperAdminLogoutController,
    SuperAdminManagersController,
    SuperAdminManagerDetailController,
    SuperAdminModulesController,
    SuperAdminRolesController,
)

urlpatterns = [
    # Auth
    path('login/', SuperAdminLoginController.as_view(), name='super-admin-login'),
    path('logout/', SuperAdminLogoutController.as_view(), name='super-admin-logout'),
    path('profile/', SuperAdminProfileController.as_view(), name='super-admin-profile'),

    # Managers & Faculty
    path('managers/', SuperAdminManagersController.as_view(), name='super-admin-managers'),
    path('managers/<int:pk>/', SuperAdminManagerDetailController.as_view(), name='super-admin-manager-detail'),

    # Roles & Modules
    path('modules/', SuperAdminModulesController.as_view(), name='super-admin-modules'),
    path('roles/', SuperAdminRolesController.as_view(), name='super-admin-roles'),
]
