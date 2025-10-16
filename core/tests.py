from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Project, Trade, Issue, Comment, Attachment

User = get_user_model()


class ProjectTests(APITestCase):
    def setUp(self):
        Project.objects.all().delete()
        self.user = User.objects.create_user(
            username='projectmanager',
            email='manager@construction.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            project_name='Test Building',
            description='Office building construction',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
    
    def test_list_projects(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        # Handle pagination - response.data contains 'results' key
        results = response.data.get('results', response.data)
        project_count = Project.objects.count()
        self.assertEqual(len(results), project_count)


class TradeTests(APITestCase):
    def setUp(self):
        Trade.objects.all().delete()
        self.user = User.objects.create_user(
            username='trader',
            email='trade@construction.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.trade = Trade.objects.create(name='ELECTRICAL')
    
    def test_list_trades(self):
        response = self.client.get('/api/trades/')
        self.assertEqual(response.status_code, 200)
        # Handle pagination
        results = response.data.get('results', response.data)
        trade_count = Trade.objects.count()
        self.assertEqual(len(results), trade_count)


class ProjectTradeIntegrationTests(APITestCase):
    def setUp(self):
        Project.objects.all().delete()
        Trade.objects.all().delete()
        self.user = User.objects.create_user(
            username='manager',
            email='manager@construction.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            project_name='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
    
    def test_add_trade_to_project(self):
        response = self.client.post(f'/api/projects/{self.project.id}/add_trade/', {
            'trade_name': 'ELECTRICAL'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)


class IssueTests(APITestCase):
    def setUp(self):
        Issue.objects.all().delete()
        self.user = User.objects.create_user(
            username='issueuser',
            email='issue@construction.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            project_name='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
        self.issue = Issue.objects.create(
            project=self.project,
            trade='ELECTRICAL',
            issue_title='Broken Wiring',
            detailed_description='Electrical wiring needs replacement',
            priority='HIGH',
            assigned_to='ELECTRICAL',
            due_date=date.today() + timedelta(days=7),
            status='OPEN'
        )
    
    def test_list_issues(self):
        response = self.client.get('/api/issues/')
        self.assertEqual(response.status_code, 200)
        # Handle pagination
        results = response.data.get('results', response.data)
        issue_count = Issue.objects.count()
        self.assertEqual(len(results), issue_count)


class CommentTests(APITestCase):
    def setUp(self):
        Comment.objects.all().delete()
        self.user = User.objects.create_user(
            username='commentuser',
            email='comment@site.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            project_name='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
        self.issue = Issue.objects.create(
            project=self.project,
            trade='ELECTRICAL',
            issue_title='Test Issue',
            detailed_description='Test Description',
            priority='MEDIUM',
            assigned_to='ELECTRICAL',
            due_date=date.today() + timedelta(days=7),
            status='OPEN'
        )
        self.comment = Comment.objects.create(
            issue=self.issue,
            user=self.user,
            content='Initial comment'
        )
    
    def test_list_comments(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)
        # Handle pagination
        results = response.data.get('results', response.data)
        comment_count = Comment.objects.count()
        self.assertEqual(len(results), comment_count)


class AttachmentTests(APITestCase):
    def setUp(self):
        Attachment.objects.all().delete()
        self.user = User.objects.create_user(
            username='attachmentuser',
            email='attach@site.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            project_name='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
        self.issue = Issue.objects.create(
            project=self.project,
            trade='ELECTRICAL',
            issue_title='Test Issue',
            detailed_description='Test Description',
            priority='MEDIUM',
            assigned_to='ELECTRICAL',
            due_date=date.today() + timedelta(days=7),
            status='OPEN'
        )
    
    def test_list_attachments(self):
        test_file = SimpleUploadedFile(
            "list_test.txt",
            b"Content for listing",
            content_type="text/plain"
        )
        Attachment.objects.create(
            issue=self.issue,
            user=self.user,
            file=test_file
        )
        response = self.client.get('/api/attachments/')
        self.assertEqual(response.status_code, 200)
        # Handle pagination
        results = response.data.get('results', response.data)
        attachment_count = Attachment.objects.count()
        self.assertEqual(len(results), attachment_count)