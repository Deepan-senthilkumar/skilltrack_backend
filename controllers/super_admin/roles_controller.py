from rest_framework.views import APIView
from middleware.auth_middleware import IsSuperAdmin
from utils.response import send_success

SYSTEM_MODULES = [
    {"name": "Dashboard", "key": "dashboard", "order": 1},
    {"name": "Curriculum & Courses", "key": "curriculum", "order": 2},
    {"name": "Batches & Attendance", "key": "batches", "order": 3},
    {"name": "Daily Logs", "key": "daily_logs", "order": 4},
    {"name": "Assessments & Quizzes", "key": "quizzes", "order": 5},
    {"name": "Code Submissions", "key": "submissions", "order": 6},
    {"name": "Student Management", "key": "students", "order": 7},
    {"name": "Certificates", "key": "certificates", "order": 8},
    {"name": "Doubts & Support", "key": "doubts", "order": 9},
    {"name": "User Roles", "key": "roles", "order": 10},
    {"name": "Settings", "key": "settings", "order": 11},
]

SYSTEM_ROLES = [
    {
        "roleName": "Admin",
        "description": "Full administrative system access across all LMS modules.",
        "permissions": {m["key"]: {"canView": True, "canCreate": True, "canEdit": True, "canDelete": True} for m in SYSTEM_MODULES}
    },
    {
        "roleName": "Staff",
        "description": "Instructor access to assigned batches, student attendance, daily logs, and submissions.",
        "permissions": {m["key"]: {"canView": True, "canCreate": m["key"] not in ["roles", "settings"], "canEdit": m["key"] not in ["roles", "settings"], "canDelete": False} for m in SYSTEM_MODULES}
    },
    {
        "roleName": "Student",
        "description": "Learner access to view notes, run sandbox code, clear doubts, and attempt quizzes.",
        "permissions": {m["key"]: {"canView": m["key"] in ["curriculum", "quizzes", "submissions", "doubts"], "canCreate": m["key"] in ["submissions", "doubts"], "canEdit": False, "canDelete": False} for m in SYSTEM_MODULES}
    }
]


class SuperAdminModulesController(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return send_success("System modules fetched successfully.", SYSTEM_MODULES)


class SuperAdminRolesController(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return send_success("System roles fetched successfully.", SYSTEM_ROLES)
