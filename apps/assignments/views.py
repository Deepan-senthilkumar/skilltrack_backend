from django.utils import timezone
from django.db.models import Count, Avg, Q
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.curriculum.models import Problem, Module, Batch
from .models import ProblemAccess, Submission
from .permissions import IsInstructor
from .code_runner import run_and_validate_code
from .serializers import (
    ProblemAccessUpdateSerializer,
    BulkModuleUnlockSerializer,
    SubmissionSubmitSerializer,
    TestRunSerializer,
    SubmissionDetailSerializer,
    ReviewSubmissionSerializer,
    ProblemAccessControlSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProblemTestRunView(views.APIView):
    """
    Executes student code in a sandboxed runner and returns live output, errors,
    execution time, and auto-validation test result without saving a final submission.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            problem = Problem.objects.get(pk=pk)
        except Problem.DoesNotExist:
            return Response({'detail': 'Problem not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TestRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        language = serializer.validated_data.get('language') or problem.language or 'python'
        expected_output = serializer.validated_data.get('expected_output') or problem.expected_output

        result = run_and_validate_code(
            code=code,
            language=language,
            expected_output=expected_output,
            timeout_sec=5.0
        )

        return Response({
            'problem_id': problem.id,
            'problem_title': problem.title,
            'language': language,
            'is_passed': result['is_passed'],
            'status': result['status'],
            'actual_output': result['actual_output'],
            'expected_output': result['expected_output'],
            'error_detail': result['error_detail'],
            'execution_time_ms': result['execution_time_ms'],
        })


class ProblemSubmitSolutionView(views.APIView):
    """
    Student submits solution. Compiles/runs code in sandboxed runner,
    compares actual vs expected output, records execution time, full errors,
    attempt number, and persists the submission record.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            problem = Problem.objects.get(pk=pk)
        except Problem.DoesNotExist:
            return Response({'detail': 'Problem not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubmissionSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        language = serializer.validated_data.get('language') or problem.language or 'python'
        batch_id = serializer.validated_data.get('batch_id')
        notes = serializer.validated_data.get('notes', '')

        # Resolve batch if not provided
        batch = None
        if batch_id:
            batch = Batch.objects.filter(pk=batch_id).first()
        if not batch:
            batch = request.user.enrolled_batches.first()

        # Execute code in sandboxed runner
        exec_res = run_and_validate_code(
            code=code,
            language=language,
            expected_output=problem.expected_output,
            timeout_sec=5.0
        )

        # Count prior attempts for this student & problem
        prior_attempts = Submission.objects.filter(
            student=request.user,
            problem=problem
        ).count()
        attempt_number = prior_attempts + 1

        # Calculate score: 100% if passed, partial if runtime/syntax error
        score = problem.points if exec_res['is_passed'] else (2 if exec_res['status'] != 'COMPILE_ERROR' and len(code) > 20 else 0)

        submission = Submission.objects.create(
            student=request.user,
            problem=problem,
            batch=batch,
            language=language,
            submitted_code=code,
            actual_output=exec_res['actual_output'],
            expected_output=problem.expected_output,
            is_passed=exec_res['is_passed'],
            status=exec_res['status'],
            execution_time_ms=exec_res['execution_time_ms'],
            error_detail=exec_res['error_detail'],
            attempt_number=attempt_number,
            notes=notes,
            score=score
        )

        return Response(
            SubmissionDetailSerializer(submission).data,
            status=status.HTTP_201_CREATED
        )


class StudentMySubmissionsListView(generics.ListAPIView):
    """List submissions made by the authenticated student."""
    serializer_class = SubmissionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user).select_related(
            'problem__topic__module__subject', 'batch', 'reviewed_by'
        ).order_by('-submitted_at')


class StaffSubmissionListView(generics.ListAPIView):
    """
    Staff and Admin dashboard for reviewing all code submissions with full execution details.
    """
    serializer_class = SubmissionDetailSerializer
    permission_classes = [IsInstructor]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Submission.objects.all().select_related(
            'student', 'problem__topic__module__subject', 'batch', 'reviewed_by'
        ).order_by('-submitted_at')

        query_params = getattr(self.request, 'query_params', self.request.GET if hasattr(self.request, 'GET') else {})

        # Filter by Batch
        batch_id = query_params.get('batch')
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)

        # Filter by Course
        course_id = query_params.get('course')
        if course_id:
            queryset = queryset.filter(problem__topic__module__subject_id=course_id)

        # Filter by Student
        student_id = query_params.get('student')
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Filter by Problem
        problem_id = query_params.get('problem')
        if problem_id:
            queryset = queryset.filter(problem_id=problem_id)

        # Filter by Status (PASSED, FAILED, COMPILE_ERROR, RUNTIME_ERROR)
        status_param = query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param.upper())

        return queryset


class StaffSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all().select_related('student', 'problem__topic', 'batch', 'reviewed_by')
    serializer_class = SubmissionDetailSerializer
    permission_classes = [IsInstructor]


class StaffReviewSubmissionView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        try:
            sub = Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            return Response({'detail': 'Submission not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sub.status = serializer.validated_data['status']
        sub.score = serializer.validated_data.get('score', sub.score)
        sub.staff_feedback = serializer.validated_data.get('staff_feedback', '')
        sub.reviewed_at = timezone.now()
        sub.reviewed_by = request.user
        sub.save()

        return Response(SubmissionDetailSerializer(sub).data)


class StaffUpdateProblemAccessView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        try:
            problem = Problem.objects.get(pk=pk)
        except Problem.DoesNotExist:
            return Response({'detail': 'Problem not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProblemAccessUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_unlocked = serializer.validated_data['is_unlocked']
        deadline = serializer.validated_data.get('deadline')
        allow_late = serializer.validated_data.get('allow_late_submission', False)
        batch_name = serializer.validated_data.get('batch_name', 'All')

        access, _ = ProblemAccess.objects.get_or_create(problem=problem)
        access.is_unlocked = is_unlocked
        if is_unlocked and not access.unlocked_at:
            access.unlocked_at = timezone.now()
        access.deadline = deadline
        access.allow_late_submission = allow_late
        access.batch_name = batch_name
        access.save()

        return Response(ProblemAccessControlSerializer(access).data)


class StaffBulkModuleUnlockView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request):
        serializer = BulkModuleUnlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        module_id = serializer.validated_data['module_id']
        is_unlocked = serializer.validated_data['is_unlocked']
        deadline = serializer.validated_data.get('deadline')

        try:
            module = Module.objects.get(pk=module_id)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found.'}, status=status.HTTP_404_NOT_FOUND)

        problems = Problem.objects.filter(topic__module=module)
        updated_count = 0
        for p in problems:
            access, _ = ProblemAccess.objects.get_or_create(problem=p)
            access.is_unlocked = is_unlocked
            if is_unlocked and not access.unlocked_at:
                access.unlocked_at = timezone.now()
            access.deadline = deadline
            access.save()
            updated_count += 1

        return Response({
            'detail': f'Updated {updated_count} problems in module "{module.name}".',
            'is_unlocked': is_unlocked,
            'deadline': deadline
        })


class StaffAnalyticsView(views.APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        total_students = request.user.enrolled_batches.aggregate(c=Count('students', distinct=True))['c'] or 0
        total_subs = Submission.objects.count()
        passed_subs = Submission.objects.filter(is_passed=True).count()
        pass_rate = round((passed_subs / total_subs * 100), 1) if total_subs > 0 else 0

        return Response({
            'total_students': total_students,
            'total_submissions': total_subs,
            'passed_submissions': passed_subs,
            'pass_rate_percent': pass_rate,
        })
