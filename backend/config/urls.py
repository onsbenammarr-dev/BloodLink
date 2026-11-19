from django.http import JsonResponse
from django.contrib import admin
from django.urls import include, path


def accueil_api(request):
    return JsonResponse({"service": "BloodLink API", "site": "http://localhost:5173"})


urlpatterns = [
    path("", accueil_api),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/donneurs/", include("donneurs.urls")),
    path("api/etablissements/", include("etablissements.urls")),
    path("api/", include("demandes.urls")),
]