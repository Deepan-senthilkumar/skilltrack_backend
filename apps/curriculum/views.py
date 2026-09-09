from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.assignments.permissions import IsInstructor
from .models import (
    Subject, Module, Topic, Problem,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord
)
from .serializers import (
    SubjectSerializer, ModuleSerializer, TopicSerializer, ProblemSerializer,
    BatchSerializer, BatchTopicProgressSerializer, StaffDailyLogSerializer,
    StudentAttendanceRecordSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Subject / Course Views
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.filter(is_active=True).prefetch_related('modules__topics__problems')
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all().prefetch_related('modules__topics__problems')
    serializer_class = SubjectSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class StaffSubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all().prefetch_related('modules__topics', 'batches').order_by('order', 'id')
    serializer_class = SubjectSerializer
    permission_classes = [IsInstructor]


class StaffSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all().prefetch_related('modules__topics', 'batches')
    serializer_class = SubjectSerializer
    permission_classes = [IsInstructor]


# Module Views
class StaffModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all().select_related('subject').prefetch_related('topics').order_by('order', 'id')
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructor]


class StaffModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all().select_related('subject').prefetch_related('topics')
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructor]


# Topic Views
class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems', 'examples')
    serializer_class = TopicSerializer
    lookup_field = 'topic_id'
    permission_classes = [permissions.AllowAny]


class StaffTopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems', 'examples').order_by('order', 'id')
    serializer_class = TopicSerializer
    permission_classes = [IsInstructor]


class StaffTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems', 'examples')
    serializer_class = TopicSerializer
    permission_classes = [IsInstructor]


# Problem Views
class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all().select_related('topic__module__subject')
    serializer_class = ProblemSerializer
    permission_classes = [permissions.AllowAny]


class StaffProblemListCreateView(generics.ListCreateAPIView):
    queryset = Problem.objects.all().select_related('topic__module__subject').order_by('order', 'id')
    serializer_class = ProblemSerializer
    permission_classes = [IsInstructor]


class StaffProblemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all().select_related('topic__module__subject')
    serializer_class = ProblemSerializer
    permission_classes = [IsInstructor]


# Batch Views
class BatchListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        user = self.request.user
        queryset = Batch.objects.all().select_related('course').prefetch_related('staff', 'students', 'topic_progress')

        if user and user.is_authenticated:
            if getattr(user, 'is_admin', False) or getattr(user, 'is_superuser', False):
                pass  # Admin sees all
            elif getattr(user, 'is_instructor', False):
                queryset = queryset.filter(staff=user)
            else:
                queryset = queryset.filter(students=user)

        query_params = getattr(self.request, 'query_params', self.request.GET if hasattr(self.request, 'GET') else {})
        course_id = query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        status_param = query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param.upper())

        return queryset

    def perform_create(self, serializer):
        batch = serializer.save()
        # Pre-populate topic progress records for this batch
        topics = Topic.objects.filter(module__subject=batch.course)
        for t in topics:
            BatchTopicProgress.objects.get_or_create(batch=batch, topic=t)


class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all().select_related('course').prefetch_related('staff', 'students', 'topic_progress')
    serializer_class = BatchSerializer
    permission_classes = [IsInstructor]


# Batch Topic Progress Views (Independent of Attendance)
class BatchTopicProgressListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id):
        try:
            batch = Batch.objects.get(pk=batch_id)
        except Batch.DoesNotExist:
            return Response({'detail': 'Batch not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure all topics in the course have a progress record
        course_topics = Topic.objects.filter(module__subject=batch.course).order_by('order', 'id')
        for t in course_topics:
            BatchTopicProgress.objects.get_or_create(batch=batch, topic=t)

        progress_qs = BatchTopicProgress.objects.filter(batch=batch).select_related('topic', 'marked_by')
        serializer = BatchTopicProgressSerializer(progress_qs, many=True)
        return Response(serializer.data)


class BatchTopicProgressToggleView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request, batch_id, topic_id):
        try:
            batch = Batch.objects.get(pk=batch_id)
            topic = Topic.objects.get(pk=topic_id)
        except (Batch.DoesNotExist, Topic.DoesNotExist):
            return Response({'detail': 'Batch or Topic not found.'}, status=status.HTTP_404_NOT_FOUND)

        progress, _ = BatchTopicProgress.objects.get_or_create(batch=batch, topic=topic)
        is_completed = request.data.get('is_completed')
        if is_completed is None:
            is_completed = not progress.is_completed

        progress.is_completed = bool(is_completed)
        progress.completed_at = timezone.now() if progress.is_completed else None
        progress.marked_by = request.user
        if 'remarks' in request.data:
            progress.remarks = request.data['remarks']
        progress.save()

        return Response(BatchTopicProgressSerializer(progress).data)


# Staff Daily Task / Performance Tracking Views
class StaffDailyLogListCreateView(views.APIView):
    permission_classes = [IsInstructor]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        queryset = StaffDailyLog.objects.all().select_related('batch', 'course', 'staff', 'topic').prefetch_related('student_attendance_records')

        if not request.user.is_admin:
            queryset = queryset.filter(staff=request.user)

        # Filters
        batch_id = request.query_params.get('batch')
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)

        course_id = request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        staff_id = request.query_params.get('staff')
        if staff_id and request.user.is_admin:
            queryset = queryset.filter(staff_id=staff_id)

        date_param = request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)

        month_param = request.query_params.get('month')  # format: YYYY-MM
        if month_param:
            try:
                year, month = map(int, month_param.split('-'))
                queryset = queryset.filter(date__year=year, date__month=month)
            except ValueError:
                pass

        year_param = request.query_params.get('year')
        if year_param:
            try:
                queryset = queryset.filter(date__year=int(year_param))
            except ValueError:
                pass

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = StaffDailyLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        batch_id = data.get('batch')

        try:
            batch = Batch.objects.get(pk=batch_id)
        except Batch.DoesNotExist:
            return Response({'detail': 'Invalid batch.'}, status=status.HTTP_400_BAD_REQUEST)

        data['course'] = batch.course.id
        data['staff'] = request.user.id
        if 'total_enrolled' not in data or not data['total_enrolled']:
            data['total_enrolled'] = batch.students.count()

        serializer = StaffDailyLogSerializer(data=data)
        if serializer.is_valid():
            log = serializer.save(staff=request.user, course=batch.course)

            # Process optional per-student attendance list
            student_records = request.data.get('student_attendance', [])
            for item in student_records:
                student_id = item.get('student_id')
                is_present = item.get('is_present', True)
                remarks = item.get('remarks', '')
                if student_id:
                    StudentAttendanceRecord.objects.update_or_create(
                        daily_log=log,
                        student_id=student_id,
                        defaults={'is_present': is_present, 'remarks': remarks}
                    )

            return Response(StaffDailyLogSerializer(log).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDailyLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StaffDailyLog.objects.all().select_related('batch', 'course', 'staff', 'topic')
    serializer_class = StaffDailyLogSerializer
    permission_classes = [IsInstructor]


# Daily Multi-Batch Admin Matrix Overview
class DailyBatchMatrixView(views.APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = timezone.now().date()
        else:
            target_date = timezone.now().date()

        batches = Batch.objects.filter(status='ACTIVE').select_related('course').prefetch_related('staff', 'students')
        logs = StaffDailyLog.objects.filter(date=target_date).select_related('batch', 'course', 'staff', 'topic')
        log_by_batch = {log.batch_id: log for log in logs}

        matrix = []
        for b in batches:
            log = log_by_batch.get(b.id)
            matrix.append({
                'batch_id': b.id,
                'batch_name': b.name,
                'course_name': b.course.name,
                'schedule': b.schedule,
                'staff_names': [s.display_name for s in b.staff.all()],
                'total_enrolled': b.students.count(),
                'has_entry': bool(log),
                'session_type': log.session_type if log else 'Not Logged',
                'session_title': log.session_title if log else '',
                'students_attended': log.students_attended if log else 0,
                'remarks': log.remarks if log else '',
                'log_id': log.id if log else None,
                'staff_logged': log.staff.display_name if log else None,
            })

        return Response({
            'date': str(target_date),
            'total_batches': len(batches),
            'logged_batches': len(logs),
            'matrix': matrix
        })


# Multi-Dimensional Reporting (Daily, Monthly, Yearly)
class ReportingAnalyticsView(views.APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        view_type = request.query_params.get('view', 'daily')  # 'daily', 'monthly', 'yearly'
        batch_id = request.query_params.get('batch')
        course_id = request.query_params.get('course')
        staff_id = request.query_params.get('staff')

        queryset = StaffDailyLog.objects.all().select_related('batch', 'course', 'staff')

        if not request.user.is_admin:
            queryset = queryset.filter(staff=request.user)
        elif staff_id:
            queryset = queryset.filter(staff_id=staff_id)

        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Summary KPIs
        total_sessions = queryset.count()
        total_enrolled_sum = queryset.aggregate(s=Sum('total_enrolled'))['s'] or 0
        total_attended_sum = queryset.aggregate(s=Sum('students_attended'))['s'] or 0
        overall_attendance_pct = round((total_attended_sum / total_enrolled_sum * 100), 1) if total_enrolled_sum > 0 else 0

        # Submissions metrics
        from apps.assignments.models import Submission
        subs = Submission.objects.all()
        if batch_id:
            subs = subs.filter(batch_id=batch_id)
        total_subs = subs.count()
        passed_subs = subs.filter(is_passed=True).count()
        avg_exec_time = subs.aggregate(a=Avg('execution_time_ms'))['a'] or 0.0

        # Detailed rows based on view_type
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serialized_logs = StaffDailyLogSerializer(page, many=True).data

        return paginator.get_paginated_response({
            'kpis': {
                'total_sessions': total_sessions,
                'total_enrolled_sum': total_enrolled_sum,
                'total_attended_sum': total_attended_sum,
                'overall_attendance_pct': overall_attendance_pct,
                'total_submissions': total_subs,
                'passed_submissions': passed_subs,
                'avg_execution_time_ms': round(avg_exec_time, 2),
            },
            'view_type': view_type,
            'logs': serialized_logs
        })
