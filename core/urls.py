from django.urls import path, include
from .views import ProjectViewSet, TradeViewSet, IssueViewSet, CommentViewSet, AttachmentViewSet, register_user, project_issues
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
    path('api/', include(router.urls)),
    path('api/projects/<int:project_id>/issues/', project_issues, name='project-issues'),
]
