from django.urls import path, include
from .views import ProjectViewSet, TradeViewSet, IssueViewSet, CommentViewSet, AttachmentViewSet, register_user, project_issues, add_trade_to_project, assign_issue, upload_attachment, issue_comments, user_profile,test_assigned_projects
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import dashboard


router = DefaultRouter()

router.register(r'projects', ProjectViewSet,)
router.register(r'trades', TradeViewSet,)
router.register(r'issues', IssueViewSet,)
router.register(r'comments', CommentViewSet,)
router.register(r'attachments', AttachmentViewSet,)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/profile/', user_profile, name='user-profile'),
    path('api/projects/<int:project_id>/issues/', project_issues, name='project-issues'),
    path('api/projects/<int:project_id>/add_trade/', add_trade_to_project, name='add-trade-to-project'),
    path('api/issues/<int:issue_id>/assign/', assign_issue, name='assign-issue'),
    path('api/issues/<int:issue_id>/upload/', upload_attachment, name='upload-attachment'),
    path('api/issues/<int:issue_id>/comments/', issue_comments, name='issue-comments'),
    path('api/test-assigned-projects/', test_assigned_projects, name='test-assigned-projects'),
    path('api/', include(router.urls)),
]