from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class File(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    file_name = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads')
    file_type = models.CharField(null=True, max_length=35)
    file_size = models.FloatField(null=True)
    is_public = models.BooleanField(default=False, null=True)
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

    @property
    def download_url(self):
        return f"/files/download/{self.id}"

    def __str__(self):
        return self.file_name
    

class Folder(models.Model):
    folder_name = models.CharField(max_length=50)
    color = models.CharField(
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                regex="#[a-fA-F0-9]{6}$",
                message='Color must be in HEX format with #. Ex: #FFFFFF'
            )
        ]
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null = True
    )
    parent_folder = models.ForeignKey(
        'Folder',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.folder_name


class SharedWith(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null = True
    )
    folder = models.ForeignKey(
        'Folder',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    file = models.ForeignKey(
        'File',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'folder', 'file'], 
                name='Unique share'
            ),
            models.UniqueConstraint(
                fields=['user', 'file'],
                name='unique_without_folder'
            ),
            models.UniqueConstraint(
                fields=['user', 'folder'],
                name='unique_without_file'
            ),
        ]

    def __str__(self):
        if self.file is not None:
            return f"'{self.file}' shared with {self.user}"
        if self.folder is not None:
            return f"'{self.folder}' shared with {self.user}"
