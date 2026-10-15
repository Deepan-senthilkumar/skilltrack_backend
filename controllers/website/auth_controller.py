from apps.users.views import (
    CustomTokenObtainPairView,
    RegisterView,
    StudentRegisterView,
    MeView,
)
from rest_framework_simplejwt.views import TokenRefreshView

WebsiteLoginController = CustomTokenObtainPairView
WebsiteRegisterController = RegisterView
WebsiteStudentRegisterController = StudentRegisterView
WebsiteMeController = MeView
WebsiteTokenRefreshController = TokenRefreshView
