from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from apps.curriculum.views import serve_media_file


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "SkillStack Backend API",
        "version": "1.0.0"
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.curriculum.urls')),
    path('api/', include('apps.assignments.urls')),

    # Dedicated persistent media routes (serves in dev and prod on Render with DEBUG=False)
    re_path(r'^media/(?P<path>.*)$', serve_media_file, name='media-serve'),
    re_path(r'^api/media/(?P<path>.*)$', serve_media_file, name='api-media-serve'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


