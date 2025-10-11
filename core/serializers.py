from rest_framework import serializers
from .models import Project, Trade, Issue, Comment, Attachment

class ProjectSerializer(serializers.ModelSerializer):
    class meta:
        model = Project
        fields ='__all__'
        
class TradeSerializer(serializers.ModelSerializer):
    class meta:
        model = Trade
        fields ='__all__'
        
class IssueSerializer(serializers.ModelSerializer):
    class meta:
        model =
        fields ='__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class meta:
        model = Comment
        fields = '__all_'
        
class AttachmentSerializer(serializers.ModelSerializer):
    class meta:
        model = Attachment
        fields ='__all__'
        