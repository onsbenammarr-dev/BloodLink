from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .relances_views import DonneursARelancerView
from .views import DashboardView, DemandeSangViewSet, DonViewSet, RendezVousViewSet

router = DefaultRouter()
router.register("demandes", DemandeSangViewSet, basename="demande")
router.register("rendez-vous", RendezVousViewSet, basename="rendezvous")
router.register("dons", DonViewSet, basename="don")

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),
    path("donneurs-a-relancer/", DonneursARelancerView.as_view()),
    path("", include(router.urls)),
]