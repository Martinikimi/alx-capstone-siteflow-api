# core/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserAuthenticationTests(APITestCase):
    def test_user_registration(self):
        """Test that users can register successfully"""
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'email': 'test@siteflow.com', 
            'password': 'securepassword123'
        })
        
        # Check if registration was successful
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertTrue(User.objects.filter(email='test@siteflow.com').exists())
        
    def test_user_registration_missing_fields(self):
        """Test registration fails with missing fields"""
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            # Missing email and password
        })
        self.assertEqual(response.status_code, 400)  # 400 Bad Request

class IssueFilterTests(APITestCase):
    def setUp(self):
        """Create test user and login"""
        self.user = User.objects.create_user(
            username='testmanager',
            email='manager@construction.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_issue_list_requires_login(self):
        """Test that issues require authentication"""
        # Logout
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/issues/')
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized

class CommentTests(APITestCase):
    def setUp(self):
        """Create test user and login"""
        self.user = User.objects.create_user(
            username='commentuser',
            email='comment@site.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_comment_list_requires_login(self):
        """Test that comments require authentication"""
        # Logout
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized