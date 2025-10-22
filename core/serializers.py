from rest_framework import serializers
from .models import Project, Trade, Issue, Comment, Attachment, CustomUser, Notification, IssueHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role', 'specialty', 'is_active']
        read_only_fields = ['id', 'is_active']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    trades = serializers.PrimaryKeyRelatedField(many=True, queryset=Trade.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), required=False)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'description', 'start_date', 'end_date', 'trades', 'assigned_users']

class IssueSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            'id','project_name', 'trade', 'issue_title', 
            'detailed_description', 'priority', 'due_date',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

class CommentSerializer(serializers.ModelSerializer):
    # Show user email instead of just ID
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'user', 'user_email', 'content', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

class AttachmentSerializer(serializers.ModelSerializer):
    # Show user email and file info
    user_email = serializers.CharField(source='user.email', read_only=True)
    file_name = serializers.CharField(source='file.name', read_only=True)
    
    class Meta:
        model = Attachment
        fields = ['id', 'issue', 'user', 'user_email', 'file', 'file_name', 'uploaded_at']
        read_only_fields = ['id', 'user', 'uploaded_at']

class NotificationSerializer(serializers.ModelSerializer):
    # Show issue title instead of just ID
    issue_title = serializers.CharField(source='issue.issue_title', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'issue', 'issue_title', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class IssueHistorySerializer(serializers.ModelSerializer):
    # Show user email and issue title
    user_email = serializers.CharField(source='user.email', read_only=True)
    issue_title = serializers.CharField(source='issue.issue_title', read_only=True)
    
    class Meta:
        model = IssueHistory
        fields = ['id', 'issue', 'issue_title', 'user', 'user_email', 'action', 'old_value', 'new_value', 'timestamp']
        read_only_fields = ['id', 'timestamp']