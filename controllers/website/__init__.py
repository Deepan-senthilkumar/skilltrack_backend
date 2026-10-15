from .auth_controller import (
    WebsiteLoginController,
    WebsiteRegisterController,
    WebsiteStudentRegisterController,
    WebsiteMeController,
    WebsiteTokenRefreshController,
)
from .curriculum_controller import (
    WebsiteSubjectListController,
    WebsiteSubjectDetailController,
    WebsiteTopicDetailController,
    WebsiteProblemDetailController,
)
from .quiz_controller import (
    WebsiteTopicQuizStartController,
    WebsiteTopicQuizSubmitController,
    WebsiteStudentTopicProgressController,
)
from .coderunner_controller import (
    WebsiteCodeTestRunController,
    WebsiteCodeSubmitController,
    WebsiteMySubmissionsController,
)
from .doubt_controller import (
    WebsiteTopicDoubtListCreateController,
    WebsiteTopicDoubtStaffListController,
    WebsiteTopicDoubtReplyController,
)
from .certificate_controller import (
    WebsiteMyEnrollmentsController,
    WebsiteEnrollCourseController,
    WebsiteMyCertificatesController,
    WebsiteCertificateDetailController,
    WebsiteGenerateCertificateController,
    WebsiteStaffEnrollmentListCreateController,
    WebsiteStaffEnrollmentDetailController,
    WebsiteStaffCertificateListCreateController,
    WebsiteStaffCertificateDetailController,
)
from .analytics_controller import (
    WebsitePlatformCapabilitiesController,
    WebsiteReportingAnalyticsController,
)

__all__ = [
    "WebsiteLoginController",
    "WebsiteRegisterController",
    "WebsiteStudentRegisterController",
    "WebsiteMeController",
    "WebsiteTokenRefreshController",
    "WebsiteSubjectListController",
    "WebsiteSubjectDetailController",
    "WebsiteTopicDetailController",
    "WebsiteProblemDetailController",
    "WebsiteTopicQuizStartController",
    "WebsiteTopicQuizSubmitController",
    "WebsiteStudentTopicProgressController",
    "WebsiteCodeTestRunController",
    "WebsiteCodeSubmitController",
    "WebsiteMySubmissionsController",
    "WebsiteTopicDoubtListCreateController",
    "WebsiteTopicDoubtStaffListController",
    "WebsiteTopicDoubtReplyController",
    "WebsiteMyEnrollmentsController",
    "WebsiteEnrollCourseController",
    "WebsiteMyCertificatesController",
    "WebsiteCertificateDetailController",
    "WebsiteGenerateCertificateController",
    "WebsiteStaffEnrollmentListCreateController",
    "WebsiteStaffEnrollmentDetailController",
    "WebsiteStaffCertificateListCreateController",
    "WebsiteStaffCertificateDetailController",
    "WebsitePlatformCapabilitiesController",
    "WebsiteReportingAnalyticsController",
]
