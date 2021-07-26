from django.urls import path
from .api.views import ReadView

urlpatterns = [
    path("read/<str:code>", ReadView.as_view(), name="read"),
]
