from django.contrib import admin
from .models import File, Folder, SharedWith

admin.site.register(File)
admin.site.register(Folder)
admin.site.register(SharedWith)