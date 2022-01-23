from django.db import models
from django.conf import settings

class File(models.Model):
    file_name = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads')
    file_type = models.CharField(null=True, max_length=35)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    parent_folder = models.ForeignKey(
        'Folder',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.file_name

class Folder(models.Model):
    foler_name = models.CharField(max_length=50)
    parent_folder = models.ForeignKey(
        'Folder',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.folder_name