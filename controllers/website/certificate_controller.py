from apps.curriculum.views import (
    MyEnrollmentsListView,
    EnrollCourseView,
    MyCertificatesListView,
    CertificateDetailView,
    GenerateCertificateView,
    StaffEnrollmentListCreateView,
    StaffEnrollmentDetailView,
    StaffCertificateListCreateView,
    StaffCertificateDetailView,
)

WebsiteMyEnrollmentsController = MyEnrollmentsListView
WebsiteEnrollCourseController = EnrollCourseView
WebsiteMyCertificatesController = MyCertificatesListView
WebsiteCertificateDetailController = CertificateDetailView
WebsiteGenerateCertificateController = GenerateCertificateView

# Staff enrollment and certificate views
WebsiteStaffEnrollmentListCreateController = StaffEnrollmentListCreateView
WebsiteStaffEnrollmentDetailController = StaffEnrollmentDetailView
WebsiteStaffCertificateListCreateController = StaffCertificateListCreateView
WebsiteStaffCertificateDetailController = StaffCertificateDetailView
