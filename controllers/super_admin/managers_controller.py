from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.users.serializers import UserSerializer, StaffUserCreateSerializer, AdminUserManageSerializer
from middleware.auth_middleware import IsSuperAdmin
from utils.response import send_success, send_error

User = get_user_model()


class SuperAdminManagersController(APIView):
    """
    CRUD controller for Platform Managers / Instructors / Staff.
    """
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        queryset = User.objects.filter(role__in=['ADMIN', 'STAFF']).select_related('assigned_subject').order_by('-date_joined')
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(mobile_number__icontains=search)
            )
        serializer = UserSerializer(queryset, many=True)
        return send_success("Managers fetched successfully.", serializer.data)

    def post(self, request):
        serializer = StaffUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return send_success("Manager created successfully.", UserSerializer(user).data, status_code=status.HTTP_201_CREATED)
        return send_error("Validation failed.", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class SuperAdminManagerDetailController(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            return send_success("Manager details fetched.", UserSerializer(user).data)
        except User.DoesNotExist:
            return send_error("Manager not found.", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = AdminUserManageSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = serializer.save()
                return send_success("Manager updated successfully.", UserSerializer(updated_user).data)
            return send_error("Update failed.", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except User.DoesNotExist:
            return send_error("Manager not found.", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            return send_success("Manager deactivated successfully.")
        except User.DoesNotExist:
            return send_error("Manager not found.", status_code=status.HTTP_404_NOT_FOUND)
