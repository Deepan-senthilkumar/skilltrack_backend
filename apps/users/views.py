from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from apps.assignments.permissions import IsInstructor
from .serializers import (
    UserSerializer, RegisterSerializer,
    StudentRegisterSerializer, StaffUserCreateSerializer,
    CustomTokenObtainPairSerializer
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


# Admin Faculty / Staff Team Management
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
