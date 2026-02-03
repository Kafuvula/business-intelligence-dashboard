"""
Tests for authentication module
"""

import unittest
import json
from app import create_app, db
from app.models import User
from flask import url_for

class AuthTestCase(unittest.TestCase):
    """Test case for authentication endpoints"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test client
        self.client = self.app.test_client()
        
        # Create test user
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            role='staff'
        )
        self.test_user.set_password('testpass123')
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
        
        # Verify user was created in database
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass123',
            'confirm_password': 'differentpass'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)
    
    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        response = self.client.post('/auth/register', data={
            'username': 'testuser',  # Already exists
            'email': 'different@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)
    
    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
    
    def test_user_login_wrong_password(self):
        """Test login with wrong password"""
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_user_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = self.client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'somepassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_user_logout(self):
        """Test user logout"""
        # First login
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Then logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
    
    def test_protected_route_without_login(self):
        """Test accessing protected route without login"""
        response = self.client.get('/dashboard', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
        self.assertIn(b'Sign in to your account', response.data)
    
    def test_protected_route_with_login(self):
        """Test accessing protected route after login"""
        # Login first
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Access protected route
        response = self.client.get('/dashboard')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_user_role_functionality(self):
        """Test user role-based functionality"""
        # Create admin user
        admin = User(
            username='adminuser',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()
        
        # Login as admin
        self.client.post('/auth/login', data={
            'username': 'adminuser',
            'password': 'adminpass'
        })
        
        # Admin should have admin privileges
        user = User.query.filter_by(username='adminuser').first()
        self.assertTrue(user.is_admin())
        self.assertTrue(user.is_manager())
        
        # Login as regular staff
        self.client.get('/auth/logout')
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Staff should not have admin privileges
        user = User.query.filter_by(username='testuser').first()
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_manager())

if __name__ == '__main__':
    unittest.main()