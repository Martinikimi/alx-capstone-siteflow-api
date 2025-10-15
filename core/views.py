from django.shortcuts import render
from rest_framework import viewsets
from .models import Project,Trade,Issue,Comment, Attachment
from .serializers import ProjectSerializer, TradeSerializer, IssueSerializer, CommentSerializer, AttachmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    # Get the data from the form
    data = request.data
    
    # Create the user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # Add the role and specialty
    user.role = data['role']
    user.specialty = data.get('specialty', 'GENERAL')
    user.save()
    
    return Response({
        'message': 'User created!',
        'user_id': user.id
    })
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes =[IsAuthenticated]
class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes =[IsAuthenticated]
    
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes =[IsAuthenticated]
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes =[IsAuthenticated]
    
    