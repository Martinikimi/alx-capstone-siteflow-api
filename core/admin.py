from django.contrib import admin
from .models import CustomUser, Project,Trade, Issue, Comment, Attachment

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Trade)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Attachment)
