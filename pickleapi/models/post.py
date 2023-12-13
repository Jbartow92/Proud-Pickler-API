# models.py

from django.db import models
from .court import Court  # Adjust the import based on your actual import structure

class Post(models.Model):
    """Database model for tracking events"""

    pickle_user = models.ForeignKey("PickleUser", on_delete=models.CASCADE, related_name="posts")
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True, related_name="courts")
    title = models.CharField(max_length=200)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField()
    content = models.CharField(max_length=200)
    categories = models.ManyToManyField("Category", through="PostCategory", related_name="posts")
