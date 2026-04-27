from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from recipes_app.models import Recipe

class RecipeAPITestCaseHappy (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +self.token.key)
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=self.user)

    def test_recipes_list(self):
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipes_post(self):
        url = reverse('recipe-list')
        data = {'title':'Recipe1',
                'description': '1Component',
                'author': self.user.id}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_recipes_detail(self):
        url = reverse('recipe-detail', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecipeAPITestCaseUnhappy (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Frank', password='1234')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=self.user)

    def test_recipes_post(self):
        url = reverse('recipe-list')
        data = {'title':'Recipe1',
                'description': '1Component',
                'author': self.user.id}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipes_detail(self):
        url = reverse('recipe-detail', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)