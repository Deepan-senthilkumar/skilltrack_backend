from apps.assignments import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.assignments.permissions import IsInstructor
from .serializers import (
    UserSerializer, RegisterSerializer,
    StudentRegisterSerializer, StaffUserCreateSerializer,
    CustomTokenObtainPairSerializer, AdminUserManageSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class StudentRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({
                'message': 'Student registered successfully. You can now log in using your Mobile Number and PIN.',
                'user': user_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'mobile_number' in data:
            user.mobile_number = data['mobile_number']
        if 'bio' in data:
            user.bio = data['bio']
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)


# Admin User Management (Staff and Students CRUD)
class AdminUserListCreateView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        role = request.query_params.get('role')
        queryset = User.objects.all().order_by('-date_joined')
        if role:
            queryset = queryset.filter(role=role.upper())
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
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminUserManageSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserDetailView(APIView):
    permission_classes = [IsInstructor]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminUserManageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(UserSerializer(updated_user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# Legacy / direct helper views
class StudentListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_instructor:
            return User.objects.filter(id=user.id)
        return User.objects.filter(role='STUDENT').order_by('-date_joined')


class StaffStudentCreateView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsInstructor]

    def perform_create(self, serializer):
        serializer.save(role='STUDENT')


class StaffStudentDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(role='STUDENT')
    permission_classes = [IsInstructor]


class StaffFacultyListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return User.objects.filter(role='STAFF').order_by('-date_joined')


class StaffFacultyCreateView(generics.CreateAPIView):
    serializer_class = StaffUserCreateSerializer
    permission_classes = [IsInstructor]


class StaffFacultyDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(role='STAFF')
    permission_classes = [IsInstructor]
