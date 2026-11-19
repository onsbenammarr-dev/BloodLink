from django.urls import path
from .views import MonEtablissementView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("me/", MonEtablissementView.as_view()),
]