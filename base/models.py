from django.db import models

language_choices = [
    ('fa', 'Persian'),
    ('en', 'English')
]


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=50)
    slogan = models.CharField(max_length=250)
    banner_image = models.ImageField(upload_to='media/', default='media/hero-bg.jpg')
    image = models.ImageField(upload_to='media/')
    about_up = models.TextField()
    about_down = models.TextField()
    about_img = models.ImageField(upload_to='media/')
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    video = models.FileField(upload_to='media/', blank=True, null=True)


class Category(models.Model):
    title = models.CharField(max_length=250)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    def __str__(self):
        return self.title

class About_item(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=250)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    bootstrap_icon = models.CharField(max_length=100, blank=True, default='bi-diagram-3')
    order = models.PositiveIntegerField(default=0)


class Customer(models.Model):
    image = models.ImageField(upload_to='media/costumers')
    name = models.CharField(max_length=50)


class Service(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1024)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    bootstrap_icon = models.CharField(max_length=100, null=True, default='bi-easel')
    order = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=250)
    short_description = models.TextField(max_length=1024, blank=True)
    description = models.TextField(max_length=1024)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    image = models.ImageField(upload_to='media/products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False)


class Member(models.Model):
    name = models.CharField(max_length=250)
    position = models.CharField(max_length=1024)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    linkedin_link = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='media/members')
    order = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False)


class Pricing(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1024)
    price = models.FloatField(blank=True, null=True)
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    order = models.PositiveIntegerField(default=0)


class Information(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='media/information')
    language = models.CharField(
        max_length=10,
        choices=language_choices,
    )
    order = models.PositiveIntegerField(default=0)
