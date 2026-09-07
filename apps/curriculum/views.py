from rest_framework import generics, permissions, status
from rest_framework.response import Response
from apps.assignments.permissions import IsInstructor
from apps.assignments.models import ProblemAccess
from .models import Subject, Module, Topic, Problem, CodeExample
from .serializers import (
    SubjectSerializer, SubjectDetailSerializer, SubjectWriteSerializer,
    ModuleSerializer, ModuleWriteSerializer,
    TopicSerializer, TopicWriteSerializer,
    ProblemSerializer, ProblemWriteSerializer,
    CodeExampleSerializer
)


class SubjectListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.filter(is_active=True).order_by('order', 'id')


class SubjectDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectDetailSerializer
    queryset = Subject.objects.filter(is_active=True)
    lookup_field = 'slug'


class CurriculumOverviewView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ModuleSerializer

    def get_queryset(self):
        qs = Module.objects.prefetch_related(
            'topics__examples', 'topics__problems__access_control'
        ).all().order_by('order', 'id')

        subject_slug = self.request.query_params.get('subject')
        if subject_slug:
            qs = qs.filter(subject__slug=subject_slug)
        elif self.request.user.is_authenticated and self.request.user.is_instructor and self.request.user.assigned_subject:
            # Default staff to their assigned subject if they have one and didn't specify
            qs = qs.filter(subject=self.request.user.assigned_subject)
        elif not subject_slug:
            # By default show Django subject curriculum
            django_sub = Subject.objects.filter(slug='django').first()
            if django_sub:
                qs = qs.filter(subject=django_sub)
        return qs


class TopicDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TopicSerializer
    lookup_field = 'topic_id'

    def get_queryset(self):
        return Topic.objects.prefetch_related('examples', 'problems__access_control').all()


class ProblemDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProblemSerializer
    queryset = Problem.objects.select_related('topic__module', 'access_control').all()


# Staff CRUD Endpoints
class StaffModuleCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = ModuleWriteSerializer
    queryset = Module.objects.all()


class StaffModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructor]
    serializer_class = ModuleWriteSerializer
    queryset = Module.objects.all()


class StaffTopicCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = TopicWriteSerializer
    queryset = Topic.objects.all()


class StaffTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructor]
    serializer_class = TopicWriteSerializer
    queryset = Topic.objects.all()


class StaffProblemCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = ProblemWriteSerializer
    queryset = Problem.objects.all()

    def perform_create(self, serializer):
        problem = serializer.save()
        ProblemAccess.objects.get_or_create(problem=problem, defaults={'is_unlocked': False})


class StaffProblemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructor]
    serializer_class = ProblemWriteSerializer
    queryset = Problem.objects.all()


class StaffCodeExampleCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = CodeExampleSerializer
    queryset = CodeExample.objects.all()


class StaffCodeExampleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructor]
    serializer_class = CodeExampleSerializer
    queryset = CodeExample.objects.all()


class StaffSubjectCreateView(generics.CreateAPIView):
    permission_classes = [IsInstructor]
    serializer_class = SubjectWriteSerializer
    queryset = Subject.objects.all()


class StaffSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructor]
    serializer_class = SubjectWriteSerializer
    queryset = Subject.objects.all()
