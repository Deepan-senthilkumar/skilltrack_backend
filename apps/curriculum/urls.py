from django.urls import path
from .views import (
    SubjectListView, SubjectDetailView, StaffSubjectListCreateView, StaffSubjectDetailView,
    StaffModuleListCreateView, StaffModuleDetailView,
    TopicDetailView, StaffTopicListCreateView, StaffTopicDetailView,
    GenericImageUploadView, TopicImageUploadView, TopicImageDeleteView, TopicImageListView,
    StaffCodeExampleListCreateView, StaffCodeExampleDetailView,
    ProblemDetailView, StaffProblemListCreateView, StaffProblemDetailView,
    BatchListCreateView, BatchDetailView,
    BatchTopicProgressListView, BatchTopicProgressToggleView,
    StaffDailyLogListCreateView, StaffDailyLogDetailView,
    DailyBatchMatrixView, ReportingAnalyticsView,
    PlatformCapabilityListView,
    StaffTopicQuizQuestionListCreateView, StaffTopicQuizQuestionDetailView,
    StaffBulkUploadQuizQuestionsView, TopicQuizStartView, TopicQuizSubmitView,
    StudentTopicProgressListView, StaffQuizAttemptAnalyticsView, StaffResetQuizCooldownView
)

urlpatterns = [
    # Courses / Subjects
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<slug:slug>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('staff/subjects/', StaffSubjectListCreateView.as_view(), name='staff-subject-list-create'),
    path('staff/subjects/<int:pk>/', StaffSubjectDetailView.as_view(), name='staff-subject-detail'),

    # Modules
    path('staff/modules/', StaffModuleListCreateView.as_view(), name='staff-module-list-create'),
    path('staff/modules/<int:pk>/', StaffModuleDetailView.as_view(), name='staff-module-detail'),

    # Topics
    path('curriculum/topics/<slug:topic_id>/', TopicDetailView.as_view(), name='topic-detail'),
    path('staff/topics/', StaffTopicListCreateView.as_view(), name='staff-topic-list-create'),
    path('staff/topics/<int:pk>/', StaffTopicDetailView.as_view(), name='staff-topic-detail'),

    # Topic Images & Generic Image Upload
    path('staff/upload-image/', GenericImageUploadView.as_view(), name='generic-image-upload'),
    path('staff/topics/<int:topic_id>/images/', TopicImageUploadView.as_view(), name='topic-image-upload'),
    path('staff/topics/<int:topic_id>/images/list/', TopicImageListView.as_view(), name='topic-image-list'),
    path('staff/topic-images/<int:pk>/delete/', TopicImageDeleteView.as_view(), name='topic-image-delete'),

    # Code Examples (Practical Code)
    path('staff/code-examples/', StaffCodeExampleListCreateView.as_view(), name='staff-code-example-list-create'),
    path('staff/code-examples/<int:pk>/', StaffCodeExampleDetailView.as_view(), name='staff-code-example-detail'),

    # Problems (Practice Programs)
    path('curriculum/problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-detail'),
    path('staff/problems/', StaffProblemListCreateView.as_view(), name='staff-problem-list-create'),
    path('staff/problems/<int:pk>/', StaffProblemDetailView.as_view(), name='staff-problem-detail'),

    # Topic Quiz Bank & Knowledge Gate (MCQs)
    path('staff/quiz-questions/', StaffTopicQuizQuestionListCreateView.as_view(), name='staff-quiz-question-list-create'),
    path('staff/quiz-questions/<int:pk>/', StaffTopicQuizQuestionDetailView.as_view(), name='staff-quiz-question-detail'),
    path('staff/quiz-questions/bulk/', StaffBulkUploadQuizQuestionsView.as_view(), name='staff-quiz-questions-bulk-upload'),
    
    # Student Quiz Execution & Secured Knowledge Gate
    path('curriculum/topics/<slug:topic_id>/quiz/start/', TopicQuizStartView.as_view(), name='topic-quiz-start'),
    path('curriculum/topics/<slug:topic_id>/quiz/submit/', TopicQuizSubmitView.as_view(), name='topic-quiz-submit'),
    path('my-topic-progress/', StudentTopicProgressListView.as_view(), name='student-topic-progress-list'),

    # Staff Quiz Analytics & Cooldown Controls
    path('staff/quiz-analytics/', StaffQuizAttemptAnalyticsView.as_view(), name='staff-quiz-analytics'),
    path('staff/quiz-cooldown/reset/', StaffResetQuizCooldownView.as_view(), name='staff-quiz-cooldown-reset'),

    # Batches (Duplicate courses running in parallel across batches)
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch-detail'),

    # Topic Progress Tracking (Independent of attendance)
    path('batches/<int:batch_id>/progress/', BatchTopicProgressListView.as_view(), name='batch-topic-progress-list'),
    path('batches/<int:batch_id>/topics/<int:topic_id>/toggle/', BatchTopicProgressToggleView.as_view(), name='batch-topic-progress-toggle'),

    # Staff Daily Task / Performance Tracking
    path('staff-logs/', StaffDailyLogListCreateView.as_view(), name='staff-daily-log-list-create'),
    path('staff-logs/<int:pk>/', StaffDailyLogDetailView.as_view(), name='staff-daily-log-detail'),
    path('staff-logs/matrix/', DailyBatchMatrixView.as_view(), name='daily-batch-matrix'),

    # Multi-Dimensional Reports & Analytics
    path('reports/analytics/', ReportingAnalyticsView.as_view(), name='reporting-analytics'),

    # Public Website APIs
    path('platform/capabilities/', PlatformCapabilityListView.as_view(), name='platform-capabilities'),
]
