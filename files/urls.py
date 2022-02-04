from telnetlib import DO
from django.urls import path
from .views import (
    ListCreateFiles, 
    ListCreateFolders, 
    RetrieveContentInFolder,
    RetrieveUpdateDestroyFile,
    RetrieveUpdateDestroyFolder,
    DownloadFile,
    ShareFile,
    ShareFolder
    )

urlpatterns = [
    path('files/', ListCreateFiles.as_view(), name="listcreatefiles"),
    path('files/<int:pk>', RetrieveUpdateDestroyFile.as_view(), name="retrieveupdatedestroyfile"),
    path('files/<int:pk>/download', DownloadFile.as_view(), name="downloadfile"),
    path('files/<int:pk>/share', ShareFile.as_view(), name="sharefile"),
    path('folders/', ListCreateFolders.as_view(), name="listcreatefolders"),
    path('folders/<int:pk>', RetrieveUpdateDestroyFolder.as_view(), name="retrieveupdatedestroyfolder"),
    path('folders/<int:pk>/content', RetrieveContentInFolder.as_view(), name="retrievefilesinfolder"),
    path('folders/<int:pk>/share', ShareFolder.as_view(), name="sharefolder"),
]