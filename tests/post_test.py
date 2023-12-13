import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from pickleapi.models import PickleUser

class PostTests(APITestCase):

    fixtures = ['user', 'token','pickleusers', 'categories', 'posts',]

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = PickleUser.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_create_posts(self):
        url = "/posts"

        data = {
           
            "category": 1,
            "title": "New Test Post",
            "court": 0,
            "publication_date": "2023-03-01",
            "image_url": "http://www.testimage.jpeg",
            "content": "Here is the content for test post",
            "categories": [2, 1],
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["pickleusers"]["user"]["id"], self.user.id)
        self.assertEqual(json_response["title"], "New Test Post")
        self.assertEqual(
                json_response["court"],
                {
                    "pk": 1,
                    "fields": {
                        "title": "1st court",
                        "city": "Nashville",
                        "state": "TN",
                        "number_of_courts": 10,
                        "open_hours": "9am - 6pm",
                        "court_image_url": "http://first.com",
                    },
                }
            )
        self.assertEqual(json_response["image_url"], "http://www.testimage.jpeg")
        self.assertEqual(json_response["content"], "Here is the content for test post")
        self.assertEqual(json_response["categories"], [{'id': 1, 'label': 'Doubles'}, {'id': 2, 'label': 'Singles'}])
        

    def test_get_all_posts(self):
        response = self.client.get("/posts")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["title"], "first post")

