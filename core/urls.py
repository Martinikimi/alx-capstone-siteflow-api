from django.urls import path, include
from .views import ProjectViewSet, TradeViewSet, IssueViewSet, CommentViewSet, AttachmentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'projects', ProjectViewSet,)
router.register(r'trades', TradeViewSet,)
router.register(r'issues', IssueViewSet,)
router.register(r'comments', CommentViewSet,)
router.register(r'attachments', AttachmentViewSet,)

urlpatterns = [
    path('api/', include(router.urls)),
]
