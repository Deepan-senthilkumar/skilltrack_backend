from datetime import datetime, timedelta
import random
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.assignments.permissions import IsInstructor
from .models import (
    Subject, Module, Topic, CodeExample, Problem, TopicImage,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord,
    PlatformCapability, TopicQuizQuestion, StudentTopicProgress, TopicQuizAttempt
)
from .serializers import (
    SubjectSerializer, ModuleSerializer, TopicSerializer, CodeExampleSerializer, ProblemSerializer,
    BatchSerializer, BatchTopicProgressSerializer, StaffDailyLogSerializer,
    StudentAttendanceRecordSerializer, TopicImageSerializer,
    PlatformCapabilitySerializer,
    TopicQuizQuestionSerializer, StudentQuizQuestionSerializer,
    StudentTopicProgressSerializer, TopicQuizAttemptSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Subject / Course Views
class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Subject.objects.filter(is_active=True).annotate(
            annotated_batch_count=Count('batches', distinct=True),
            annotated_topic_count=Count('modules__topics', distinct=True),
            annotated_module_count=Count('modules', distinct=True)
        ).prefetch_related(
            'modules__topics__problems__access_control',
            'modules__topics__examples',
            'modules__topics__images',
            'batches'
        ).order_by('order', 'id')


class SubjectDetailView(generics.RetrieveAPIView):
    serializer_class = SubjectSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Subject.objects.annotate(
            annotated_batch_count=Count('batches', distinct=True),
            annotated_topic_count=Count('modules__topics', distinct=True),
            annotated_module_count=Count('modules', distinct=True)
        ).prefetch_related(
            'modules__topics__problems__access_control',
            'modules__topics__examples',
            'modules__topics__images',
            'batches'
        )


class StaffSubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Subject.objects.annotate(
            annotated_batch_count=Count('batches', distinct=True),
            annotated_topic_count=Count('modules__topics', distinct=True),
            annotated_module_count=Count('modules', distinct=True)
        ).prefetch_related(
            'modules__topics__problems__access_control',
            'modules__topics__examples',
            'modules__topics__images',
            'batches'
        ).order_by('order', 'id')


class StaffSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Subject.objects.annotate(
            annotated_batch_count=Count('batches', distinct=True),
            annotated_topic_count=Count('modules__topics', distinct=True),
            annotated_module_count=Count('modules', distinct=True)
        ).prefetch_related(
            'modules__topics__problems__access_control',
            'modules__topics__examples',
            'modules__topics__images',
            'batches'
        )


# Module Views
class StaffModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all().select_related('subject').prefetch_related(
        'topics__problems__access_control',
        'topics__examples',
        'topics__images'
    ).order_by('order', 'id')
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructor]


class StaffModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all().select_related('subject').prefetch_related(
        'topics__problems__access_control',
        'topics__examples',
        'topics__images'
    )
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructor]


# Topic Views
class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems__access_control', 'examples', 'images')
    serializer_class = TopicSerializer
    lookup_field = 'topic_id'
    permission_classes = [permissions.AllowAny]


class StaffTopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems__access_control', 'examples', 'images').order_by('order', 'id')
    serializer_class = TopicSerializer
    permission_classes = [IsInstructor]


class StaffTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all().select_related('module__subject').prefetch_related('problems__access_control', 'examples', 'images')
    serializer_class = TopicSerializer
    permission_classes = [IsInstructor]


# Topic Image Upload / Delete Views
def save_uploaded_image_file(image_file, subfolder="topic_images", request=None):
    """
    Saves uploaded image file to Django media storage.
    Optionally tries Supabase, but falls back gracefully to local media to guarantee 100% success.
    """
    import os, uuid
    from django.conf import settings
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile

    ext = os.path.splitext(image_file.name)[1].lower() or '.jpg'
    filename = f"{uuid.uuid4().hex}{ext}"
    relative_path = f"{subfolder}/{filename}"

    try:
        saved_path = default_storage.save(relative_path, ContentFile(image_file.read()))
        media_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path.lstrip('/')}"
        if request:
            return request.build_absolute_uri(media_url)
        return media_url
    except Exception:
        # Direct filesystem fallback
        target_dir = os.path.join(settings.MEDIA_ROOT, subfolder)
        os.makedirs(target_dir, exist_ok=True)
        disk_path = os.path.join(target_dir, filename)
        image_file.seek(0)
        with open(disk_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        media_url = f"{settings.MEDIA_URL.rstrip('/')}/{subfolder}/{filename}"
        if request:
            return request.build_absolute_uri(media_url)
        return media_url


class GenericImageUploadView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request):
        image_file = request.FILES.get('image') or request.FILES.get('file')
        if not image_file:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        caption = request.data.get('caption', '')
        topic_id = request.data.get('topic_id') or request.data.get('topic')

        public_url = save_uploaded_image_file(image_file, subfolder="notes_images", request=request)

        created_img_id = None
        if topic_id:
            try:
                topic = Topic.objects.get(pk=int(topic_id))
                order = int(request.data.get('order', TopicImage.objects.filter(topic=topic).count() + 1))
                img = TopicImage.objects.create(
                    topic=topic,
                    image_url=public_url,
                    caption=caption,
                    order=order
                )
                created_img_id = img.id
            except (Topic.DoesNotExist, ValueError):
                pass

        return Response({
            'id': created_img_id,
            'image_url': public_url,
            'caption': caption,
            'status': 'success'
        }, status=status.HTTP_201_CREATED)


class TopicImageUploadView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request, topic_id):
        try:
            topic = Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        image_file = request.FILES.get('image') or request.FILES.get('file')
        if not image_file:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        caption = request.data.get('caption', '')
        order = int(request.data.get('order', TopicImage.objects.filter(topic=topic).count() + 1))

        public_url = save_uploaded_image_file(image_file, subfolder=f"topic_{topic_id}", request=request)

        img = TopicImage.objects.create(
            topic=topic,
            image_url=public_url,
            caption=caption,
            order=order
        )

        return Response(TopicImageSerializer(img).data, status=status.HTTP_201_CREATED)


class TopicImageDeleteView(views.APIView):
    permission_classes = [IsInstructor]

    def delete(self, request, pk):
        try:
            img = TopicImage.objects.get(pk=pk)
        except TopicImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        img.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)


class TopicImageListView(generics.ListAPIView):
    serializer_class = TopicImageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        return TopicImage.objects.filter(topic_id=topic_id).order_by('order', 'id')


# Code Example (Practical Code) Views
class StaffCodeExampleListCreateView(generics.ListCreateAPIView):
    serializer_class = CodeExampleSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        # pyrefly: ignore [missing-attribute]
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            return CodeExample.objects.filter(topic_id=topic_id).order_by('order', 'id')
        return CodeExample.objects.all().order_by('order', 'id')


class StaffCodeExampleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeExample.objects.all()
    serializer_class = CodeExampleSerializer
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

    def perform_create(self, serializer):
        problem = serializer.save()
        from apps.assignments.models import ProblemAccess
        # pyrefly: ignore [missing-attribute]
        is_unlocked = self.request.data.get('is_unlocked', True)
        if isinstance(is_unlocked, str):
            is_unlocked = is_unlocked.lower() in ('true', '1', 'yes')
        access, _ = ProblemAccess.objects.get_or_create(problem=problem)
        access.is_unlocked = bool(is_unlocked)
        access.allow_late_submission = True
        if access.is_unlocked and not access.unlocked_at:
            access.unlocked_at = timezone.now()
        access.save()


class StaffProblemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all().select_related('topic__module__subject')
    serializer_class = ProblemSerializer
    permission_classes = [IsInstructor]

    def perform_update(self, serializer):
        problem = serializer.save()
        # pyrefly: ignore [missing-attribute]
        if 'is_unlocked' in self.request.data:
            from apps.assignments.models import ProblemAccess
            # pyrefly: ignore [missing-attribute]
            is_unlocked = self.request.data.get('is_unlocked')
            if isinstance(is_unlocked, str):
                is_unlocked = is_unlocked.lower() in ('true', '1', 'yes')
            access, _ = ProblemAccess.objects.get_or_create(problem=problem)
            access.is_unlocked = bool(is_unlocked)
            if access.is_unlocked and not access.unlocked_at:
                access.unlocked_at = timezone.now()
            access.save()



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


# Public Website API: Platform Capabilities (Feature Cards)
class PlatformCapabilityListView(generics.ListAPIView):
    """Returns active capability/feature cards for the website homepage."""
    queryset = PlatformCapability.objects.filter(is_active=True).order_by('order', 'id')
    serializer_class = PlatformCapabilitySerializer
    permission_classes = [permissions.AllowAny]


# =========================================================================
# TOPIC QUIZ / KNOWLEDGE GATE SYSTEM
# =========================================================================

class StaffTopicQuizQuestionListCreateView(generics.ListCreateAPIView):
    """Staff / Admin: List and create MCQs for topic question banks"""
    serializer_class = TopicQuizQuestionSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        queryset = TopicQuizQuestion.objects.select_related('topic', 'topic__module', 'topic__module__subject').all()
        if topic_id:
            if topic_id.isdigit():
                queryset = queryset.filter(topic_id=int(topic_id))
            else:
                queryset = queryset.filter(topic__topic_id=topic_id)
        return queryset.order_by('topic', 'order', 'id')


class StaffTopicQuizQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Staff / Admin: Retrieve, update, or delete a single MCQ"""
    queryset = TopicQuizQuestion.objects.all()
    serializer_class = TopicQuizQuestionSerializer
    permission_classes = [IsInstructor]


class StaffBulkUploadQuizQuestionsView(views.APIView):
    """Staff / Admin: Bulk upload MCQs for a topic (e.g. 20+ questions)"""
    permission_classes = [IsInstructor]

    def post(self, request):
        topic_id = request.data.get('topic_id')
        questions = request.data.get('questions', [])

        if not topic_id or not questions:
            return Response({'error': 'topic_id and a list of questions are required'}, status=status.HTTP_400_BAD_REQUEST)

        topic = None
        if str(topic_id).isdigit():
            topic = Topic.objects.filter(id=int(topic_id)).first()
        else:
            topic = Topic.objects.filter(topic_id=str(topic_id)).first()

        if not topic:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        created_objs = []
        current_max_order = TopicQuizQuestion.objects.filter(topic=topic).count()

        for idx, q_data in enumerate(questions):
            q_text = q_data.get('question_text', '').strip()
            opt_a = q_data.get('option_a', '').strip()
            opt_b = q_data.get('option_b', '').strip()
            opt_c = q_data.get('option_c', '').strip()
            opt_d = q_data.get('option_d', '').strip()
            correct = q_data.get('correct_option', 'A').strip().upper()
            expl = q_data.get('explanation', '').strip()
            order = q_data.get('order') or (current_max_order + idx + 1)

            if q_text and opt_a and opt_b:
                created_objs.append(TopicQuizQuestion(
                    topic=topic,
                    question_text=q_text,
                    option_a=opt_a,
                    option_b=opt_b,
                    option_c=opt_c or 'N/A',
                    option_d=opt_d or 'N/A',
                    correct_option=correct if correct in ['A', 'B', 'C', 'D'] else 'A',
                    explanation=expl,
                    order=order
                ))

        if created_objs:
            TopicQuizQuestion.objects.bulk_create(created_objs)

        total_now = TopicQuizQuestion.objects.filter(topic=topic).count()
        return Response({
            'success': True,
            'created_count': len(created_objs),
            'total_questions_in_bank': total_now,
            'message': f'Successfully added {len(created_objs)} questions. Topic now has {total_now} total questions.'
        })


class TopicQuizStartView(views.APIView):
    """Student: Starts a randomized 5-question test for a topic in the Secured Test Portal"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, topic_id):
        topic = None
        if str(topic_id).isdigit():
            topic = Topic.objects.filter(id=int(topic_id)).first()
        else:
            topic = Topic.objects.filter(topic_id=str(topic_id)).first()

        if not topic:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        # 1. Check Cooldown
        progress = StudentTopicProgress.objects.filter(student=request.user, topic=topic).first()
        if progress and progress.is_in_cooldown:
            remaining = progress.cooldown_seconds_remaining()
            return Response({
                'in_cooldown': True,
                'cooldown_seconds_remaining': remaining,
                'can_reattempt_after': progress.can_reattempt_after,
                'error': f'Re-attempt cooldown active. Please re-read the study notes. You can re-attempt in {remaining // 60}m {remaining % 60}s.'
            }, status=status.HTTP_403_FORBIDDEN)

        # 2. Fetch question bank
        all_questions = list(TopicQuizQuestion.objects.filter(topic=topic))
        if not all_questions:
            return Response({
                'error': 'No assessment questions configured for this topic yet. Please contact trainer/admin.',
                'question_count': 0
            }, status=status.HTTP_400_BAD_REQUEST)

        # 3. Random sample 5 questions from the bank (or all if < 5)
        num_to_sample = min(5, len(all_questions))
        sampled_questions = random.sample(all_questions, num_to_sample)

        serializer = StudentQuizQuestionSerializer(sampled_questions, many=True)
        return Response({
            'topic_id': topic.id,
            'topic_title': topic.title,
            'topic_slug': topic.topic_id,
            'total_questions_in_bank': len(all_questions),
            'questions_served_count': num_to_sample,
            'pass_percentage_required': 50.0,
            'min_score_required': (num_to_sample + 1) // 2,
            'cooldown_minutes_on_fail': 10,
            'questions': serializer.data
        })


class TopicQuizSubmitView(views.APIView):
    """Student: Evaluates answers for the topic quiz, records attempt, and updates progression & cooldown"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, topic_id):
        topic = None
        if str(topic_id).isdigit():
            topic = Topic.objects.filter(id=int(topic_id)).first()
        else:
            topic = Topic.objects.filter(topic_id=str(topic_id)).first()

        if not topic:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        answers = data.get('answers', {})  # { "12": "A", "15": "C" }
        question_ids = data.get('question_ids', [])
        time_taken = int(data.get('time_taken_seconds', 0))
        security_violations = int(data.get('security_violations', 0))
        violation_details = str(data.get('violation_details', ''))
        is_terminated_by_security = bool(data.get('is_terminated_by_security', False))

        now = timezone.now()
        progress, _ = StudentTopicProgress.objects.get_or_create(student=request.user, topic=topic)

        # If security violation failure
        if is_terminated_by_security or security_violations >= 2:
            status_code = 'FAILED_SECURITY'
            is_passed = False
            score = 0
            total_questions = len(question_ids) or 5
            percentage = 0.0
            cooldown_until = now + timedelta(minutes=10)

            progress.attempts_count += 1
            progress.last_score = 0
            progress.last_total = total_questions
            progress.last_percentage = 0.0
            progress.last_passed = False
            progress.can_reattempt_after = cooldown_until
            progress.save()

            attempt = TopicQuizAttempt.objects.create(
                student=request.user,
                topic=topic,
                score=0,
                total_questions=total_questions,
                percentage=0.0,
                is_passed=False,
                status=status_code,
                security_violations=security_violations,
                violation_details=violation_details or "Terminated due to multiple tab switches or window exits.",
                questions_data=[],
                selected_answers=answers,
                time_taken_seconds=time_taken
            )

            return Response({
                'is_passed': False,
                'status': status_code,
                'score': 0,
                'total_questions': total_questions,
                'percentage': 0.0,
                'security_violations': security_violations,
                'can_reattempt_after': cooldown_until,
                'cooldown_seconds_remaining': 600,
                'message': '❌ Test Terminated: Security violations detected. You must wait 10 minutes before re-attempting.'
            })

        # Fetch actual question objects
        if not question_ids:
            question_ids = [int(qid) for qid in answers.keys() if str(qid).isdigit()]

        questions = TopicQuizQuestion.objects.filter(id__in=question_ids, topic=topic)
        total_questions = len(questions) or 1
        score = 0
        questions_review = []
        questions_snapshot = []

        for q in questions:
            user_choice = str(answers.get(str(q.id)) or answers.get(q.id) or '').strip().upper()
            is_correct = (user_choice == q.correct_option)
            if is_correct:
                score += 1

            review_item = {
                'id': q.id,
                'question_text': q.question_text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'user_choice': user_choice,
                'correct_option': q.correct_option,
                'is_correct': is_correct,
                'explanation': q.explanation
            }
            questions_review.append(review_item)
            questions_snapshot.append(review_item)

        percentage = round((score / total_questions * 100), 1)
        is_passed = (percentage >= 50.0)
        status_code = 'PASSED' if is_passed else 'FAILED_SCORE'

        if is_passed:
            cooldown_until = None
            progress.is_completed = True
            if not progress.completed_at:
                progress.completed_at = now
        else:
            cooldown_until = now + timedelta(minutes=10)

        progress.attempts_count += 1
        progress.last_score = score
        progress.last_total = total_questions
        progress.last_percentage = percentage
        progress.last_passed = is_passed
        progress.can_reattempt_after = cooldown_until
        progress.save()

        attempt = TopicQuizAttempt.objects.create(
            student=request.user,
            topic=topic,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            is_passed=is_passed,
            status=status_code,
            security_violations=security_violations,
            violation_details=violation_details,
            questions_data=questions_snapshot,
            selected_answers=answers,
            time_taken_seconds=time_taken
        )

        return Response({
            'attempt_id': attempt.id,
            'is_passed': is_passed,
            'status': status_code,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'pass_threshold_percentage': 50.0,
            'security_violations': security_violations,
            'can_reattempt_after': cooldown_until,
            'cooldown_seconds_remaining': progress.cooldown_seconds_remaining(),
            'review': questions_review,
            'topic_completed': progress.is_completed,
            'message': '🎉 Congratulations! You passed the topic assessment!' if is_passed else '❌ You did not reach the 50% pass mark. Please re-read the study notes.'
        })


class StudentTopicProgressListView(generics.ListAPIView):
    """Student: Returns all topic completion and cooldown statuses for the student"""
    serializer_class = StudentTopicProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentTopicProgress.objects.filter(student=self.request.user).select_related('topic')


class StaffQuizAttemptAnalyticsView(views.APIView):
    """Staff / Admin: Detailed logs and metrics of all student quiz attempts"""
    permission_classes = [IsInstructor]

    def get(self, request):
        topic_id = request.query_params.get('topic_id')
        student_id = request.query_params.get('student_id')
        status_filter = request.query_params.get('status')
        search = request.query_params.get('search', '').strip()

        queryset = TopicQuizAttempt.objects.select_related('student', 'topic', 'topic__module', 'topic__module__subject').all()

        if topic_id:
            if topic_id.isdigit():
                queryset = queryset.filter(topic_id=int(topic_id))
            else:
                queryset = queryset.filter(topic__topic_id=topic_id)

        if student_id and student_id.isdigit():
            queryset = queryset.filter(student_id=int(student_id))

        if status_filter and status_filter != 'ALL':
            queryset = queryset.filter(status=status_filter)

        if search:
            queryset = queryset.filter(
                Q(student__username__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__mobile_number__icontains=search) |
                Q(topic__title__icontains=search)
            )

        # Summary KPIs
        total_attempts = queryset.count()
        passed_attempts = queryset.filter(is_passed=True).count()
        failed_attempts = total_attempts - passed_attempts
        pass_rate_pct = round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0
        avg_score_pct = round(queryset.aggregate(a=Avg('percentage'))['a'] or 0.0, 1)
        security_infractions_sum = queryset.aggregate(s=Sum('security_violations'))['s'] or 0

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serialized_attempts = TopicQuizAttemptSerializer(page, many=True).data

        return paginator.get_paginated_response({
            'kpis': {
                'total_attempts': total_attempts,
                'passed_attempts': passed_attempts,
                'failed_attempts': failed_attempts,
                'pass_rate_pct': pass_rate_pct,
                'avg_score_pct': avg_score_pct,
                'security_infractions_sum': security_infractions_sum,
            },
            'attempts': serialized_attempts
        })


class StaffResetQuizCooldownView(views.APIView):
    """Staff / Admin: Clear cooldown timer for a student on a specific topic"""
    permission_classes = [IsInstructor]

    def post(self, request):
        student_id = request.data.get('student_id')
        topic_id = request.data.get('topic_id')

        if not student_id or not topic_id:
            return Response({'error': 'student_id and topic_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        topic_filter = {'id': int(topic_id)} if str(topic_id).isdigit() else {'topic_id': str(topic_id)}
        topic = Topic.objects.filter(**topic_filter).first()
        if not topic:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        progress = StudentTopicProgress.objects.filter(student_id=student_id, topic=topic).first()
        if not progress:
            return Response({'error': 'No progress record found for this student and topic'}, status=status.HTTP_404_NOT_FOUND)

        progress.can_reattempt_after = None
        progress.save()

        return Response({
            'success': True,
            'message': f'Successfully cleared cooldown for student on topic: {topic.title}'
        })

