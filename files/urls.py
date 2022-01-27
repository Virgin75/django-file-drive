from telnetlib import DO
from django.urls import path
from .views import (
    ListCreateFiles, 
    ListCreateFolders, 
    RetrieveFilesInFolder,
    RetrieveUpdateDestroyFile,
    DownloadFile
    )

urlpatterns = [
    path('files/', ListCreateFiles.as_view(), name="listcreatefiles"),
    path('files/<int:pk>', RetrieveUpdateDestroyFile.as_view(), name="retrieveupdatedestroyfile"),
    path('files/download/<int:pk>', DownloadFile.as_view(), name="downloadfile"),
    path('folders/', ListCreateFolders.as_view(), name="listcreatefolders"),
    path('folders/<int:pk>', RetrieveFilesInFolder.as_view(), name="retrievefilesinfolder"),
]