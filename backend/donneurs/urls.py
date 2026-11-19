from django.urls import path
from .views import RegisterDonneurView

urlpatterns = [path("register/", RegisterDonneurView.as_view())]