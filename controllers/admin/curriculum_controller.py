from apps.curriculum.views import (
    StaffSubjectListCreateView,
    StaffSubjectDetailView,
    StaffModuleListCreateView,
    StaffModuleDetailView,
    StaffTopicListCreateView,
    StaffTopicDetailView,
    StaffCodeExampleListCreateView,
    StaffCodeExampleDetailView,
    GenericImageUploadView,
    TopicImageUploadView,
    TopicImageDeleteView,
    TopicImageListView,
)

# Admin / Staff Curriculum Controllers
AdminSubjectListCreateController = StaffSubjectListCreateView
AdminSubjectDetailController = StaffSubjectDetailView
AdminModuleListCreateController = StaffModuleListCreateView
AdminModuleDetailController = StaffModuleDetailView
AdminTopicListCreateController = StaffTopicListCreateView
AdminTopicDetailController = StaffTopicDetailView
AdminCodeExampleListCreateController = StaffCodeExampleListCreateView
AdminCodeExampleDetailController = StaffCodeExampleDetailView
AdminGenericImageUploadController = GenericImageUploadView
AdminTopicImageUploadController = TopicImageUploadView
AdminTopicImageDeleteController = TopicImageDeleteView
AdminTopicImageListView = TopicImageListView
