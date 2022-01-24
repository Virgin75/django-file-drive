from django.urls import path
from .views import ListCreateFiles, ListCreateFolders, RetrieveFilesInFolder

urlpatterns = [
    path('files/', ListCreateFiles.as_view(), name="listcreatefiles"),
    path('folders/', ListCreateFolders.as_view(), name="listcreatefolders"),
    path('folders/<int:pk>', RetrieveFilesInFolder.as_view(), name="retrievefilesinfolder"),
]