from django.shortcuts import render
from rest_framework import viewsets
from .models import Project,Trade,Issue,Comment, Attachment
from .serializers import ProjectSerializer, TradeSerializer, IssueSerializer, CommentSerializer, AttachmentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from .filters import IssueFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import IssueFilter
from .filters import CommentFilter

def dashboard(request):
    return render(request, 'core/dashboard.html')

User = get_user_model()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method =='GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_trade_to_project(request, project_id):
    """
    Add a trade to a specific project
    POST /api/projects/1/add_trade/
    {
        "trade_name": "ELECTRICAL"
    }
    """

    # STEP 1: Check if project exists
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # STEP 2: Get the trade name from request
    trade_name = request.data.get('trade_name')
    
    if not trade_name:
        return Response(
            {"error": "Trade name is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # STEP 3: Create the trade and link it to the project
    try:
        # Create the trade or get existing one
        trade, created = Trade.objects.get_or_create(
            name=trade_name,
            project=project
        )
        
        # STEP 4: Return success message
        if created:
            message = f"Trade '{trade_name}' added to project '{project.project_name}'"
        else:
            message = f"Trade '{trade_name}' already exists in project '{project.project_name}'"
        
        return Response({
            "message": message,
            "project_id": project.id,
            "project_name": project.project_name,
            "trade_name": trade_name,
            "trade_id": trade.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to add trade: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = IssueFilter
    search_fields = ['issue_title', 'detailed_description']
    ordering_fields = ['priority', 'due_date', 'created_at']

    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_issue(request, issue_id):
    """
    Assign or reassign an issue to a trade
    POST /api/issues/15/assign/
    {
        "assigned_trade": "ELECTRICAL"
    }
    """

    # STEP 1: Check if issue exists
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        return Response(
            {"error": "Issue not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # STEP 2: Get the trade from request
    assigned_trade = request.data.get('assigned_trade')
    
    if not assigned_trade:
        return Response(
            {"error": "assigned_trade is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # STEP 3: Validate it's a valid trade choice - FIXED LINE!
    valid_trades = [choice[0] for choice in Issue._meta.get_field('assigned_to').choices]
    if assigned_trade not in valid_trades:
        return Response(
            {"error": f"Invalid trade. Must be one of: {', '.join(valid_trades)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # STEP 4: Create audit trail (optional)
    try:
        IssueHistory.objects.create(
            issue=issue,
            user=request.user,
            action="assigned_trade_changed",
            old_value=issue.assigned_to,
            new_value=assigned_trade
        )
    except:
        pass  # Skip audit if it fails
    
    # STEP 5: Save the old assignment and update
    old_assignment = issue.assigned_to
    issue.assigned_to = assigned_trade
    issue.save()
    
    # STEP 6: Return success response
    return Response({
        "message": f"Issue #{issue_id} assigned to {assigned_trade}",
        "issue_id": issue_id,
        "issue_title": issue.issue_title,
        "old_assignment": old_assignment,
        "new_assignment": assigned_trade,
        "project": issue.project.project_name
    }, status=status.HTTP_200_OK)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['content']
    ordering_fields = ['timestamp', 'user']
    ordering = ['-timestamp']

    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def issue_comments(request, issue_id):
    """
    Get or add comments for a specific issue
    GET /api/issues/15/comments/ - Get all comments for issue 15
    POST /api/issues/15/comments/ - Add comment to issue 15
    
    """
    
    # STEP 1: Check if issue exists
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        return Response(
            {"error": "Issue not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # STEP 2: Handle GET request (view comments)
    if request.method == 'GET':
        # Get all comments for this issue, ordered by newest first
        comments = Comment.objects.filter(issue=issue).order_by('-timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # STEP 3: Handle POST request (add comment)
    elif request.method == 'POST':
        # Get the comment content
        content = request.data.get('content')
        
        if not content:
            return Response(
                {"error": "Comment content is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # STEP 4: Create the comment
        try:
            comment = Comment.objects.create(
                issue=issue,
                user=request.user,
                content=content
            )
            
            # STEP 5: Return success
            return Response({
                "message": "Comment added successfully",
                "comment_id": comment.id,
                "content": content,
                "user": request.user.username,
                "timestamp": comment.timestamp,
                "issue_id": issue_id,
                "issue_title": issue.issue_title
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Failed to add comment: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes =[IsAuthenticated]
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_attachment(request, issue_id):
    """
    Upload a file attachment to an issue
    POST /api/issues/15/upload/
    Form Data:
    - file: (the actual file - image, PDF, etc.)
    """
    
    # STEP 1: Check if issue exists
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        return Response(
            {"error": "Issue not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # STEP 2: Check if file was provided
    if 'file' not in request.FILES:
        return Response(
            {"error": "No file provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # STEP 3: Get the uploaded file
    uploaded_file = request.FILES['file']
    
    # STEP 4: Validate file size (optional - 10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        return Response(
            {"error": "File too large. Maximum size is 10MB"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # STEP 5: Create the attachment using YOUR model
    try:
        attachment = Attachment.objects.create(
            issue=issue,
            user=request.user,  # Uses your 'user' field
            file=uploaded_file  # Uses your 'file' field
        )
        
        # STEP 6: Return success
        return Response({
            "message": "File uploaded successfully",
            "attachment_id": attachment.id,
            "file_url": attachment.file.url,  # Django automatically creates URL
            "file_name": uploaded_file.name,
            "file_size": uploaded_file.size,
            "uploaded_by": request.user.username,
            "uploaded_at": attachment.uploaded_at,
            "issue_id": issue.id,
            "issue_title": issue.issue_title
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to upload file: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )