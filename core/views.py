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
    
@api_view(['POST'])

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
    
@api_view(['POST'])
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
    
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes =[IsAuthenticated]
    
    