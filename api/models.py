from django.contrib.auth.models import User
from django.db import models

language_choices = [
    ('fa', 'Persian'),
    ('en', 'English')
]

# Create your models here.
class UserAPI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=200)
    key = models.TextField(max_length=200)

class ApiMethod(models.Model):
    route = models.TextField(max_length=200)
    test_code = models.TextField(max_length=512)
    code_result = models.TextField(max_length=512)

class ApiParam(models.Model):
    api_method = models.ForeignKey(ApiMethod, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=512)
