from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "online",
        "service": "SkillStack Backend API",
        "version": "1.0.0"
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.curriculum.urls')),
    path('api/', include('apps.assignments.urls')),
]
