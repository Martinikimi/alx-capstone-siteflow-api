from django.shortcuts import render
from rest_framework import viewsets
from .models import Project,Trade,Issue,Comment, Attachment
from .serializers import ProjectSerializer, TradeSerializer, IssueSerializer, CommentSerializer, AttachmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view


def dashboard(request):
    return render(request, 'core/dashboard.html')

User = get_user_model()
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    # Get the data from the form
    data = request.data
    
    user = User.objects.create_user(
    username=data['username'],
    email=data['email'],
    password=data['password'],
)
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
    
@api_view(['GET', 'POST'])
def project_issues(request, project_id):
    """
Handle issues for a specific project
- GET: Get all issues for this project
- POST: Create a new issue in this project
    """
    try:
        project= Project.objects.get(id = project_id)
    except Project.DoesNotExist:
        return Response(
        {"error": "Project not found"}, 
        status=status.HTTP_404_NOT_FOUND
    )
        
    if request.method =='GET':
        issues = Issue.objects.filter(project_id = project_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['project'] = project_id
        serializer = IssueSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes =[IsAuthenticated]
    
    