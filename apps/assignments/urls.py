from django.urls import path
from .views import (
    StaffUpdateProblemAccessView,
    StaffBulkModuleUnlockView,
    SubmitProblemSolutionView,
    StaffSubmissionsListView,
    StaffReviewSubmissionView,
    StudentMySubmissionsView,
    StaffAnalyticsView,
    TestRunCodeView,
)

urlpatterns = [
    # Staff problem management
    path('staff/problems/<int:pk>/access/', StaffUpdateProblemAccessView.as_view(), name='staff-problem-access'),
    path('staff/modules/unlock/', StaffBulkModuleUnlockView.as_view(), name='staff-module-unlock'),
    path('staff/submissions/', StaffSubmissionsListView.as_view(), name='staff-submissions-list'),
    path('staff/submissions/<int:pk>/review/', StaffReviewSubmissionView.as_view(), name='staff-submission-review'),
    path('staff/analytics/', StaffAnalyticsView.as_view(), name='staff-analytics'),

    # Student problem submission & automated test runner
    path('problems/<int:pk>/test-run/', TestRunCodeView.as_view(), name='student-problem-test-run'),
    path('problems/<int:pk>/submit/', SubmitProblemSolutionView.as_view(), name='student-problem-submit'),
    path('my-submissions/', StudentMySubmissionsView.as_view(), name='student-my-submissions'),
]
