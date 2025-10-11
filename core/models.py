from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class CustomUser(AbstractUser):
    ROLE_CHOICES =[
        ('ADMIN', 'admin'),
        ('PROJECT MANAGER', 'project manager'),
        ('SITE OFFICER', 'site officer'),
        ('SUB CONTRACTOR', 'subcontractor'),
    ]
    
    TRADE_SPECIALTY =[
        ('ARCHITECTURAL','architectural'),
        ('STRUCTURAL','structural'),
        ('ELECTRICAL','electrical'),
        ('MECHANICAL', 'mechanical'),
        ('PLUMBING', 'plumbing'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField (max_length=20, choices=ROLE_CHOICES, default= 'ADMIN')
    specialty = models.CharField(max_length=50, choices = TRADE_SPECIALTY, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']
    
    def __str__(self):
        return self.email


TRADE_CHOICES =[
        ('GENERAL', 'general'),
        ('ARCHITECTURAL','architectural'),
        ('STRUCTURAL', 'structural'),
        ('ELECTRICAL', 'electrical'),
        ('PLUMBING','plumbing'),
        ('HVAC', 'hvac'),
    ]
class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    trades = models.ManyToManyField('Trade')
    
    def __str__(self):
        return self.project_name
    
class Trade(models.Model):
    name = models.CharField(max_length=100, choices= TRADE_CHOICES)
    
    def __str__(self):
        return self.name

class Issue(models.Model):
    PRIORITY_STATUS =[
        ('LOW','low'),
        ('MEDIUM','medium'),
        ('HIGH','high'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    trade = models.CharField(max_length=200, choices= TRADE_CHOICES)
    issue_title = models.CharField(max_length=100, blank=False, null=False)
    detailed_description = models.TextField(blank=False, null =False)
    priority = models.CharField(max_length=100, choices=PRIORITY_STATUS)
    assigned_to = models.CharField(max_length=100,choices= TRADE_CHOICES)
    due_date = models.DateField()
    
    def __str__(self):
        return self.issue_title
class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)