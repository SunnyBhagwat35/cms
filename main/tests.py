from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from main.models import Content

class YourAppViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
        )
        self.client = APIClient()

    def test_api_overview(self):
        response = self.client.get('http://127.0.0.1:8000/cms/')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions as needed

    def test_user_registration_with_short_password(self):
        data = {'email': 'test@example.com', 'password': 'Tets', 'full_name': 'sunny bhagwat', 'phone': '1234567890', 'pincode': '400603'}
        url = reverse('user_registration')
        response = self.client.post(url, data)
        # print(response.data)
        self.assertIn(b'This password is too short', response.content)

    def test_user_registration(self):
        data = {'email': 'test@example.com', 'password': 'Test@1235', 'full_name': 'Test User', 'phone': '1234567890', 'pincode': '400603'}
        url = reverse('user_registration')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'test@example.com', response.content)

    def test_user_false_login(self):
        url = reverse('user_login')
        data = {'email': 'wrong_user@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(b'Invalid credentials', response.content)  

    def test_user_login(self):
        test_user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@1234',
        )

        url = reverse('user_login')  # Assuming 'user_login' is the name of your login view
        data = {'email': 'test@example.com', 'password': 'Test@1234'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming your login response includes a token

    def test_create_content(self):
        # Login the user or use self.test_user from setUp
        self.client.force_authenticate(user=self.test_user)

        url = reverse('create_content')  # Assuming 'create_content' is the name of your create content view

        file_content = b'Test file content'
        file_data = {'doc': ('testfile.txt', file_content, 'application/octet-stream')}

        data = {
            'title': 'Test Title', 
            'body': 'Test Body', 
            'summary': 'Test Summary', 
            'doc': SimpleUploadedFile("testfile.txt", b"file_content"), 
            'category': 'Test Category'
            }

        response = self.client.post(url, data, format='multipart')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)  # Assuming your create content response includes an 'id'


    def test_edit_content(self):
        test_content = Content.objects.create(
            user=self.test_user,
            title='Original Title',
            body='Original Body',
            summary='Original Summary',
            doc=SimpleUploadedFile("original_file.txt", b"original_file_content"),
            category='Original Category',
        )

        # Login the user or use self.test_user from setUp
        self.client.force_authenticate(user=self.test_user)

        url = reverse('edit_content', kwargs={'pk': test_content.id})  # Assuming 'edit_content' is the name of your edit content view
        data = {
            'title': 'Edited Title',
            'body': 'Edited Body',
            'summary': 'Edited Summary',
            'doc': SimpleUploadedFile("edited_file.txt", b"edited_file_content"),
            'category': 'Edited Category',
        }
        response = self.client.post(url, data, format='multipart')

        test_content.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_content.title, 'Edited Title')
        self.assertEqual(test_content.body, 'Edited Body')
        self.assertEqual(test_content.summary, 'Edited Summary')
        self.assertEqual(test_content.category, 'Edited Category')

    def test_delete_content(self):
        test_content = Content.objects.create(
            user=self.test_user,
            title='Test Title',
            body='Test Body',
            summary='Test Summary',
            category='Test Category',
        )

        self.client.force_authenticate(user=self.test_user)

        url = reverse('delete_content', kwargs={'pk': test_content.id})  # Assuming 'delete_content' is the name of your delete content view
        response = self.client.delete(url)

        deleted_content = Content.objects.filter(id=test_content.id).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(deleted_content) 

    
    def test_view_content(self):
        # Create a test content
        test_content = Content.objects.create(
            user=self.test_user,
            title='Test Title',
            body='Test Body',
            summary='Test Summary',
            category='Test Category',
        )

        # Login the user or use self.test_user from setUp
        self.client.force_authenticate(user=self.test_user)

        url = reverse('view_content', kwargs={'pk': test_content.id})  # Assuming 'view_content' is the name of your view content view
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Title')
        self.assertEqual(response.data['body'], 'Test Body')
        self.assertEqual(response.data['summary'], 'Test Summary')
        self.assertEqual(response.data['category'], 'Test Category')

    def test_search_content(self):
        test_content_1 = Content.objects.create(
            user=self.test_user,
            title='Test Title 1',
            body='Test Body 1',
            summary='Test Summary 1',
            category='Test Category 1',
        )

        test_content_2 = Content.objects.create(
            user=self.test_user,
            title='Test Title 2',
            body='Test Body 2',
            summary='Test Summary 2',
            category='Test Category 2',
        )

        self.client.force_authenticate(user=self.test_user)

        query = 'Test Title'
        url = reverse('search_content')  
        response = self.client.get(url, {'query': query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

        self.assertIn('Test Title 1', response.data[0]['title'])
        self.assertIn('Test Title 2', response.data[1]['title'])
