from django.urls import path
from .views import (
    ProblemTestRunView,
    ProblemSubmitSolutionView,
    StudentMySubmissionsListView,
    StaffSubmissionListView,
    StaffSubmissionDetailView,
    StaffReviewSubmissionView,
    StaffUpdateProblemAccessView,
    StaffBulkModuleUnlockView,
    StaffAnalyticsView,
)

urlpatterns = [
    # Student Code Runner & Submissions
    path('problems/<int:pk>/test-run/', ProblemTestRunView.as_view(), name='problem-test-run'),
    path('problems/<int:pk>/submit/', ProblemSubmitSolutionView.as_view(), name='problem-submit'),
    path('my-submissions/', StudentMySubmissionsListView.as_view(), name='my-submissions'),

    # Staff / Admin Submissions Dashboard & Auto-Validation Inspector
    path('staff/submissions/', StaffSubmissionListView.as_view(), name='staff-submission-list'),
    path('staff/submissions/<int:pk>/', StaffSubmissionDetailView.as_view(), name='staff-submission-detail'),
    path('staff/submissions/<int:pk>/review/', StaffReviewSubmissionView.as_view(), name='staff-review-submission'),
    path('staff/problems/<int:pk>/access/', StaffUpdateProblemAccessView.as_view(), name='staff-problem-access'),
    path('staff/modules/unlock/', StaffBulkModuleUnlockView.as_view(), name='staff-bulk-module-unlock'),
    path('staff/analytics/', StaffAnalyticsView.as_view(), name='staff-analytics'),
]
