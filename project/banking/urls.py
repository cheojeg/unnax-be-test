from django.urls import path
from .views import HomeView
from .api.views import ReadView

urlpatterns = [
    path("read/<str:code>", ReadView.as_view(), name="read"),
]
