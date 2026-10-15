from apps.users.views import (
    StudentListView,
    StaffStudentCreateView,
    StaffStudentDeleteView,
    AdminUserListCreateView,
    AdminUserDetailView,
)

AdminStudentListController = StudentListView
AdminStudentCreateController = StaffStudentCreateView
AdminStudentDeleteController = StaffStudentDeleteView
AdminUserListCreateController = AdminUserListCreateView
AdminUserDetailController = AdminUserDetailView
