from rest_framework import serializers
from .models import Project, Trade, Issue, Comment, Attachment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields ='__all__'
        
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields ='__all__'
        
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model =Issue
        fields ='__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all_'
        
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields ='__all__'
        