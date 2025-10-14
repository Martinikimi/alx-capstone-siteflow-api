from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
class CustomUser(AbstractUser):
    ROLE_CHOICES =[
        ('ADMIN', 'admin'),
        ('PROJECT MANAGER', 'project manager'),
        ('SITE OFFICER', 'site officer'),
        ('SUB CONTRACTOR', 'subcontractor'),
        ('SAFETY OFFICER', 'safety officer'),
    ]
    
    TRADE_SPECIALTY =[
        ('GENERAL', 'general'),
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
        ('CRITICAL', 'critical'),
    ]
    STATUS_CHOICES = [
    ('OPEN', 'Open'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
    ('CLOSED', 'Closed'),
]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    trade = models.CharField(max_length=100, choices=TRADE_CHOICES)
    issue_title = models.CharField(max_length=100, blank=False, null=False)
    detailed_description = models.TextField(blank=False, null =False)
    priority = models.CharField(max_length=100, choices=PRIORITY_STATUS)
    assigned_to = models.CharField(max_length=100,choices= TRADE_CHOICES)
    due_date = models.DateField()
    status = models.CharField(max_length= 50, choices = STATUS_CHOICES, default = 'open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.issue_title
    
class IssueHistory(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.issue.issue_title} - {self.action}"
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
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
@receiver(post_save, sender=Issue)
def issue_notifications(sender, instance, created, **kwargs):
    """
    Automatically sends notifications when issues are created or updated
    """
    if created:
        # NEW ISSUE: Notify the assigned trade
        send_notification_to_trade(
            trade=instance.assigned_to,
            title="New Issue Assigned",
            message=f"New {instance.assigned_to} issue: {instance.issue_title}",
            issue=instance
        )
        
        # Log in history
        IssueHistory.objects.create(
            issue=instance,
            user=instance.project.created_by if hasattr(instance.project, 'created_by') else None,
            action="issue_created",
            new_value=f"{instance.issue_title} - {instance.priority} priority"
        )
    
    else:
        # ISSUE UPDATED: Notify about important changes
        pass

@receiver(post_save, sender=Comment)
def comment_notifications(sender, instance, created, **kwargs):
    """
    Notify issue owners when new comments are added
    """
    if created:
        # Notify people related to this issue
        send_notification_to_trade(
            trade=instance.issue.assigned_to,
            title=" New Comment",
            message=f"New comment on {instance.issue.issue_title}",
            issue=instance.issue
        )

def send_notification_to_trade(trade, title, message, issue):
    """
    Helper function to send notifications to all users in a trade
    """
    # Find all users who specialize in this trade
    users_in_trade = CustomUser.objects.filter(
        Q(specialty=trade) | Q(role__in=['PROJECT MANAGER', 'SITE OFFICER'])
    )
    
    for user in users_in_trade:
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            issue=issue
        )
