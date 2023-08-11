from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_view(self):
        response = self.client.get(reverse('profile_details'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_details.html')

class UserProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_delete_view(self):
        response = self.client.get(reverse('profile_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_delete.html')

        response = self.client.post(reverse('profile_delete'))
        self.assertEqual(response.status_code, 302) 
