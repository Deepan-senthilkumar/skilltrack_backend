from django.urls import path
from controllers.website import (
    WebsiteLoginController,
    WebsiteRegisterController,
    WebsiteStudentRegisterController,
    WebsiteMeController,
    WebsiteTokenRefreshController,
    WebsiteSubjectListController,
    WebsiteSubjectDetailController,
    WebsiteTopicDetailController,
    WebsiteProblemDetailController,
    WebsiteTopicQuizStartController,
    WebsiteTopicQuizSubmitController,
    WebsiteStudentTopicProgressController,
    WebsiteCodeTestRunController,
    WebsiteCodeSubmitController,
    WebsiteMySubmissionsController,
    WebsiteTopicDoubtListCreateController,
    WebsiteTopicDoubtStaffListController,
    WebsiteTopicDoubtReplyController,
    WebsiteMyEnrollmentsController,
    WebsiteEnrollCourseController,
    WebsiteMyCertificatesController,
    WebsiteCertificateDetailController,
    WebsiteGenerateCertificateController,
    WebsitePlatformCapabilitiesController,
    WebsiteReportingAnalyticsController,
)

urlpatterns = [
    # Auth
    path('auth/login/', WebsiteLoginController.as_view(), name='website-auth-login'),
    path('auth/register/', WebsiteRegisterController.as_view(), name='website-auth-register'),
    path('auth/student-register/', WebsiteStudentRegisterController.as_view(), name='website-auth-student-register'),
    path('auth/refresh/', WebsiteTokenRefreshController.as_view(), name='website-auth-refresh'),
    path('auth/me/', WebsiteMeController.as_view(), name='website-auth-me'),

    # Public Curriculum & Topics
    path('subjects/', WebsiteSubjectListController.as_view(), name='website-subjects'),
    path('subjects/<slug:slug>/', WebsiteSubjectDetailController.as_view(), name='website-subject-detail'),
    path('curriculum/topics/<slug:topic_id>/', WebsiteTopicDetailController.as_view(), name='website-topic-detail'),
    path('curriculum/problems/<int:pk>/', WebsiteProblemDetailController.as_view(), name='website-problem-detail'),

    # Secured Quiz Knowledge Gate
    path('curriculum/topics/<slug:topic_id>/quiz/start/', WebsiteTopicQuizStartController.as_view(), name='website-quiz-start'),
    path('curriculum/topics/<slug:topic_id>/quiz/submit/', WebsiteTopicQuizSubmitController.as_view(), name='website-quiz-submit'),
    path('my-topic-progress/', WebsiteStudentTopicProgressController.as_view(), name='website-topic-progress'),

    # Student Code Runner Sandbox
    path('problems/<int:pk>/test-run/', WebsiteCodeTestRunController.as_view(), name='website-problem-test-run'),
    path('problems/<int:pk>/submit/', WebsiteCodeSubmitController.as_view(), name='website-problem-submit'),
    path('my-submissions/', WebsiteMySubmissionsController.as_view(), name='website-my-submissions'),

    # Doubts
    path('curriculum/topics/<slug:topic_id>/doubts/', WebsiteTopicDoubtListCreateController.as_view(), name='website-topic-doubts'),
    path('doubts/', WebsiteTopicDoubtStaffListController.as_view(), name='website-doubts-list'),
    path('doubts/<int:pk>/reply/', WebsiteTopicDoubtReplyController.as_view(), name='website-doubt-reply'),

    # Enrollments & Certificates
    path('my-enrollments/', WebsiteMyEnrollmentsController.as_view(), name='website-my-enrollments'),
    path('enroll/', WebsiteEnrollCourseController.as_view(), name='website-enroll-course'),
    path('my-certificates/', WebsiteMyCertificatesController.as_view(), name='website-my-certificates'),
    path('certificates/<str:certificate_id>/', WebsiteCertificateDetailController.as_view(), name='website-certificate-detail'),
    path('generate-certificate/', WebsiteGenerateCertificateController.as_view(), name='website-generate-certificate'),

    # Platform & Analytics
    path('platform/capabilities/', WebsitePlatformCapabilitiesController.as_view(), name='website-platform-capabilities'),
    path('reports/analytics/', WebsiteReportingAnalyticsController.as_view(), name='website-reports-analytics'),
]
