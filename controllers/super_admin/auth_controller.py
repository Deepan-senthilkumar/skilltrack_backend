from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from middleware.auth_middleware import IsSuperAdmin
from utils.response import send_success, send_error


class SuperAdminLoginController(TokenObtainPairView):
    """
    Super Admin Authentication controller.
    """
    serializer_class = CustomTokenObtainPairSerializer


class SuperAdminProfileController(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return send_success("Super admin profile fetched successfully.", user_data)


class SuperAdminLogoutController(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        return send_success("Super admin logged out successfully.")
