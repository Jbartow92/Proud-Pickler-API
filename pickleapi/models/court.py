from django.db import models



class Court(models.Model):
    """Database model for tracking events"""

    title = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    number_of_courts = models.IntegerField(null=True)
    open_hours = models.CharField(max_length=200)
    court_image_url = models.URLField()