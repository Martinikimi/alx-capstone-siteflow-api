from django.db import models
from django.contrib.auth.models import AbstractUser

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
        ('ARCHITECTURAL', 'architectural'),
        ('STRUCTURAL', 'structural'),
        ('ELECTRICAL', 'electrical'),
        ('PLUMBING','plumbing'),
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
