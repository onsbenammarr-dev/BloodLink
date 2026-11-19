from django.urls import path
from .views import ChangerMotDePasseView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("mot-de-passe/", ChangerMotDePasseView.as_view()),
]