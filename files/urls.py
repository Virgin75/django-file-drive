from django.urls import path
from .views import ListCreateFiles

urlpatterns = [
    path('', ListCreateFiles.as_view(), name="listcreatefiles"),
]