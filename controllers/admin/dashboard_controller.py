from rest_framework.views import APIView
from apps.curriculum.views import (
    StaffDailyLogListCreateView,
    StaffDailyLogDetailView,
    DailyBatchMatrixView,
    ReportingAnalyticsView,
)
from middleware.auth_middleware import IsAdminOrStaff

# Re-export and organize dashboard controllers
AdminDailyLogListCreateController = StaffDailyLogListCreateView
AdminDailyLogDetailController = StaffDailyLogDetailView
AdminDailyBatchMatrixController = DailyBatchMatrixView
AdminReportingAnalyticsController = ReportingAnalyticsView
