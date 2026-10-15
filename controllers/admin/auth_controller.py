from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from middleware.auth_middleware import IsAdminOrStaff
from utils.response import send_success


class AdminLoginController(TokenObtainPairView):
    """
    Admin and Staff login controller.
    """
    serializer_class = CustomTokenObtainPairSerializer


class AdminProfileController(APIView):
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return send_success("Profile fetched successfully.", user_data)


class AdminLogoutController(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return send_success("Logged out successfully.")
