from apps.curriculum.views import (
    StaffProblemListCreateView,
    StaffProblemDetailView,
)
from apps.assignments.views import (
    StaffSubmissionListView,
    StaffSubmissionDetailView,
    StaffReviewSubmissionView,
    StaffUpdateProblemAccessView,
    StaffBulkProblemsAccessView,
    StaffBulkModuleUnlockView,
    StaffAnalyticsView,
)

AdminProblemListCreateController = StaffProblemListCreateView
AdminProblemDetailController = StaffProblemDetailView
AdminSubmissionListController = StaffSubmissionListView
AdminSubmissionDetailController = StaffSubmissionDetailView
AdminReviewSubmissionController = StaffReviewSubmissionView
AdminUpdateProblemAccessController = StaffUpdateProblemAccessView
AdminBulkProblemsAccessController = StaffBulkProblemsAccessView
AdminBulkModuleUnlockController = StaffBulkModuleUnlockView
AdminAssignmentsAnalyticsController = StaffAnalyticsView
