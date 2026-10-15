from apps.curriculum.views import (
    StaffTopicQuizQuestionListCreateView,
    StaffTopicQuizQuestionDetailView,
    StaffBulkUploadQuizQuestionsView,
    StaffQuizAttemptAnalyticsView,
    StaffResetQuizCooldownView,
)

AdminQuizQuestionListCreateController = StaffTopicQuizQuestionListCreateView
AdminQuizQuestionDetailController = StaffTopicQuizQuestionDetailView
AdminBulkUploadQuizQuestionsController = StaffBulkUploadQuizQuestionsView
AdminQuizAttemptAnalyticsController = StaffQuizAttemptAnalyticsView
AdminResetQuizCooldownController = StaffResetQuizCooldownView
