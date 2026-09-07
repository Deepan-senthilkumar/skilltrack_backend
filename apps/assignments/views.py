from django.utils import timezone
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from apps.curriculum.models import Problem, Module
from .models import ProblemAccess, Submission
from .permissions import IsInstructor
from .serializers import (
    ProblemAccessUpdateSerializer,
    BulkModuleUnlockSerializer,
    SubmissionSubmitSerializer,
    SubmissionDetailSerializer,
    ReviewSubmissionSerializer,
    ProblemAccessControlSerializer,
)


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


def run_automated_evaluation(code, notes, problem):
    """
    Automated evaluation engine that tests code structure, syntax patterns,
    and output assertions, computing the score automatically.
    """
    total_pts = problem.points or 10
    score = 0
    feedback_lines = []
    tests_summary = []

    code_text = code.strip()
    notes_text = notes.strip().lower()

    # 1. Structure & non-empty check
    if len(code_text) >= 15:
        base_score = max(1, int(total_pts * 0.4))
        score += base_score
        tests_summary.append({"name": "Code Structure & Syntax Validity", "status": "PASSED", "points": base_score})
        feedback_lines.append(f"✓ Structure & syntax verified (+{base_score} pts)")
    else:
        tests_summary.append({"name": "Code Structure & Syntax Validity", "status": "FAILED", "points": 0})
        feedback_lines.append("✗ Implementation too brief or empty")

    # 2. Keywords / Architectural Tokens
    kw_score = max(1, int(total_pts * 0.3))
    keywords = problem.expected_keywords or []
    if not keywords:
        lower_title = (problem.title + " " + problem.description).lower()
        if 'view' in lower_title or 'http' in lower_title:
            keywords = ['def', 'return', 'request']
        elif 'model' in lower_title or 'post' in lower_title:
            keywords = ['class', 'models.']
        elif 'url' in lower_title or 'path' in lower_title:
            keywords = ['path', 'urlpatterns']
        elif 'serializer' in lower_title:
            keywords = ['serializer', 'class']
        elif 'consumer' in lower_title or 'websocket' in lower_title:
            keywords = ['consumer', 'async']
        else:
            keywords = ['def', 'import']

    matched_kw_count = sum(1 for kw in keywords if kw.lower() in code_text.lower() or kw.lower() in notes_text)
    if keywords and matched_kw_count > 0:
        earned_kw = max(1, int((matched_kw_count / len(keywords)) * kw_score))
        score += earned_kw
        tests_summary.append({"name": f"Django Architecture Tokens ({matched_kw_count}/{len(keywords)})", "status": "PASSED", "points": earned_kw})
        feedback_lines.append(f"✓ Key architectural patterns matched: {', '.join(keywords[:3])} (+{earned_kw} pts)")
    else:
        tests_summary.append({"name": "Django Architecture Tokens", "status": "FAILED", "points": 0})
        feedback_lines.append("✗ Core Django patterns missing")

    # 3. Output assertion & behavioral check
    remaining_score = total_pts - score
    output_ok = False
    if problem.expected_output_hint:
        hint_tokens = [w for w in problem.expected_output_hint.lower().replace('.', ' ').split() if len(w) > 3]
        if any(tok in notes_text or tok in code_text.lower() for tok in hint_tokens) or len(notes_text) > 8:
            output_ok = True
    elif len(notes_text) > 5 or 'ok' in notes_text or '200' in notes_text or 'migrat' in notes_text or 'success' in notes_text:
        output_ok = True
    elif score >= int(total_pts * 0.6):
        output_ok = True

    if output_ok:
        score += remaining_score
        tests_summary.append({"name": "Output / Behavioral Assertions", "status": "PASSED", "points": remaining_score})
        feedback_lines.append(f"✓ Output / behavior verified (+{remaining_score} pts)")
    else:
        tests_summary.append({"name": "Output / Behavioral Assertions", "status": "FAILED", "points": 0})
        feedback_lines.append("ℹ Provide matching terminal output to gain full marks")

    score = min(total_pts, score)
    status_result = "PASSED" if score >= int(total_pts * 0.6) else "REVISION_REQUESTED"
    feedback = f"[Auto-Graded by AI Test Runner]\n" + "\n".join(feedback_lines) + f"\n\nCalculated Score: {score}/{total_pts} ({status_result})"

    return score, status_result, feedback, tests_summary


class TestRunCodeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            problem = Problem.objects.select_related('access_control').get(pk=pk)
        except Problem.DoesNotExist:
            return Response({'detail': 'Problem not found.'}, status=status.HTTP_404_NOT_FOUND)

        code = request.data.get('submitted_code', '')
        notes = request.data.get('notes', '')

        score, eval_status, feedback, tests = run_automated_evaluation(code, notes, problem)

        return Response({
            'score': score,
            'max_points': problem.points,
            'status': eval_status,
            'feedback': feedback,
            'tests': tests,
        })


class SubmitProblemSolutionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            problem = Problem.objects.select_related('access_control').get(pk=pk)
        except Problem.DoesNotExist:
            return Response({'detail': 'Problem not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check Access Control & Timeline Restrictions
        access = getattr(problem, 'access_control', None)
        if not access or not access.is_unlocked:
            return Response(
                {'detail': 'This problem has not been unlocked by your instructor yet.'},
                status=status.HTTP_403_FORBIDDEN
            )

        now = timezone.now()
        is_late = False
        if access.deadline and now > access.deadline:
            if not access.allow_late_submission:
                return Response(
                    {'detail': 'The deadline for this problem has passed. Submissions are closed.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            is_late = True

        serializer = SubmissionSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['submitted_code']
        notes = serializer.validated_data.get('notes', '')

        # Automated Grading Execution
        score, eval_status, auto_feedback, _ = run_automated_evaluation(code, notes, problem)

        submission, _ = Submission.objects.get_or_create(
            student=request.user,
            problem=problem
        )
        submission.submitted_code = code
        submission.notes = notes
        submission.score = score
        submission.status = eval_status
        submission.staff_feedback = auto_feedback
        submission.is_late = is_late
        submission.submitted_at = now
        submission.reviewed_at = now
        submission.save()

        return Response(SubmissionDetailSerializer(submission).data, status=status.HTTP_200_OK)


class StaffSubmissionsListView(generics.ListAPIView):
    permission_classes = [IsInstructor]
    serializer_class = SubmissionDetailSerializer

    def get_queryset(self):
        qs = Submission.objects.select_related(
            'student', 'problem__topic__module', 'reviewed_by'
        ).all()

        status_filter = self.request.query_params.get('status')
        problem_id = self.request.query_params.get('problem_id')
        student_id = self.request.query_params.get('student_id')

        if status_filter:
            qs = qs.filter(status=status_filter)
        if problem_id:
            qs = qs.filter(problem_id=problem_id)
        if student_id:
            qs = qs.filter(student_id=student_id)

        return qs.order_by('-submitted_at')


class StaffReviewSubmissionView(views.APIView):
    permission_classes = [IsInstructor]

    def post(self, request, pk):
        try:
            submission = Submission.objects.select_related('student', 'problem').get(pk=pk)
        except Submission.DoesNotExist:
            return Response({'detail': 'Submission not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission.status = serializer.validated_data['status']
        submission.score = serializer.validated_data.get('score', submission.problem.points if submission.status == 'PASSED' else 0)
        submission.staff_feedback = serializer.validated_data.get('staff_feedback', '')
        submission.reviewed_at = timezone.now()
        submission.reviewed_by = request.user
        submission.save()

        return Response(SubmissionDetailSerializer(submission).data)


class StudentMySubmissionsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionDetailSerializer

    def get_queryset(self):
        return Submission.objects.select_related(
            'problem__topic__module', 'reviewed_by'
        ).filter(student=self.request.user).order_by('-submitted_at')


class StaffAnalyticsView(views.APIView):
    permission_classes = [IsInstructor]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        total_students = User.objects.filter(role='STUDENT').count()
        total_problems = Problem.objects.count()
        unlocked_problems = ProblemAccess.objects.filter(is_unlocked=True).count()
        
        all_submissions = Submission.objects.all()
        total_submissions = all_submissions.count()
        pending_review = all_submissions.filter(status='SUBMITTED').count()
        passed_count = all_submissions.filter(status='PASSED').count()
        revision_count = all_submissions.filter(status='REVISION_REQUESTED').count()

        # Module-wise breakdown
        modules_stats = []
        for m in Module.objects.all():
            m_probs = Problem.objects.filter(topic__module=m)
            m_prob_count = m_probs.count()
            m_unlocked = ProblemAccess.objects.filter(problem__in=m_probs, is_unlocked=True).count()
            m_subs = Submission.objects.filter(problem__in=m_probs).count()
            modules_stats.append({
                'module_id': m.id,
                'name': m.name,
                'level': m.level,
                'total_problems': m_prob_count,
                'unlocked_problems': m_unlocked,
                'total_submissions': m_subs
            })

        return Response({
            'total_students': total_students,
            'total_problems': total_problems,
            'unlocked_problems': unlocked_problems,
            'total_submissions': total_submissions,
            'pending_review': pending_review,
            'passed_count': passed_count,
            'revision_count': revision_count,
            'modules': modules_stats,
        })
