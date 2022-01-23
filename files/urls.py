from django.urls import path
from .views import ListCreateFiles, ListCreateFolders, RetrieveFolderWithFiles

urlpatterns = [
    path('files/', ListCreateFiles.as_view(), name="listcreatefiles"),
    path('folders/', ListCreateFolders.as_view(), name="listcreatefolders"),
    path('folders/<int:pk>', RetrieveFolderWithFiles.as_view(), name="retrieveflderwithfiles"),
]