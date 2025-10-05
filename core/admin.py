from django.contrib import admin
from .models import CustomUser, Project,Trade

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Trade)
