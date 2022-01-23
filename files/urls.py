from django.urls import path
from .views import ListCreateFiles, ListCreateFolders

urlpatterns = [
    path('my-files/', ListCreateFiles.as_view(), name="listcreatefiles"),
    path('my-folders/', ListCreateFolders.as_view(), name="listcreatefolders"),
]