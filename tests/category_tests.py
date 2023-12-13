import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from pickleapi.models import Category

class CategoryTests(APITestCase):

    fixtures = ['categories', 'user', 'token']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_categories(self):
        url = "/categories"

        data = {
            "label": "Music"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["label"], "Music")
        self.assertEqual(json_response["id"], 3)

    def test_get_category(self):
        category = Category()
        category.label = "Doubles"
        category.save()

        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Doubles")
        self.assertEqual(json_response["id"], category.id)
        
    def test_get_categories(self):
        response = self.client.get("/categories")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(json_response[0]["label"], "Doubles")
        self.assertEqual(json_response[1]["label"], "Singles")

    def test_change_categories(self):
        category = Category()
        category.label = "Doubles"
        category.save()

        data = {
            "label": "2 v 2"
        }
        response = self.client.put(f"/categories/{category.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "2 v 2")

    def test_delete_categories(self):
        category = Category()
        category.label = "Doubles"
        category.save()
        
        response = self.client.delete(f"/categories/{category.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/categories/{category.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)