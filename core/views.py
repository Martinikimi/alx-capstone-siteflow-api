from django.shortcuts import render
from rest_framework import viewsets
from .models import Project,Trade,Issue,Comment, Attachment
from .serializers import ProjectSerializer, TradeSerializer, IssueSerializer, CommentSerializer, AttachmentSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    query_set = Project.object.all()
    serializer_class = ProjectSerializer
    
class TradeViewSet(viewsets.ModelViewSet):
    query_set = Trade.object.all()
    serializer_class = TradeSerializer
    
class IssueViewSet(viewsets.ModelViewSet):
    query_set = Issue.object.all()
    serializer_class = IssueSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    query_set = Comment.object.all()
    Serializer_class = CommentSerializer
    
class AttachmentViewSet(viewsets.ModelViewSet):
    query_set = Attachment.object.all()
    Serializer_class = AttachmentSerializer
    
    