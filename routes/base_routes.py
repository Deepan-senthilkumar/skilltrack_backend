from django.urls import path, include

urlpatterns = [
    # ─── New Clean Modular Architectural Routes (Matching Backend-setup) ───
    path('super-admin/', include('routes.super_admin_routes')),
    path('admin/', include('routes.admin_routes')),
    path('website/', include('routes.website_routes')),

    # ─── Universal Compatibility Layer (Zero Breaking Changes for Live Frontends) ───
    path('', include('apps.users.urls')),
    path('', include('apps.curriculum.urls')),
    path('', include('apps.assignments.urls')),
]
