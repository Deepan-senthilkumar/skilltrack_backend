from apps.assignments.views import (
    ProblemTestRunView,
    ProblemSubmitSolutionView,
    StudentMySubmissionsListView,
)

WebsiteCodeTestRunController = ProblemTestRunView
WebsiteCodeSubmitController = ProblemSubmitSolutionView
WebsiteMySubmissionsController = StudentMySubmissionsListView
