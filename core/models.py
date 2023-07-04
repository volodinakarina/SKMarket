# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# # Create your models here.
# class User(AbstractUser):
#     REQUIRED_FIELDS = []
#
# #
# # class Ad(models.Model):
# #     title = models.CharField(max_length=100)
# #     price = models.PositiveIntegerField()
# #     description = models.TextField(max_length=2000)
# #     author = models.ForeignKey('users.User', on_delete=models.CASCADE)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     image = models.ImageField(upload_to='images/ads/', null=True, blank=True)
# #     is_active = models.BooleanField(default=True)
# #
# #     class Meta:
# #         ordering = ['-created_at']
# #
# #
# # class Comment(models.Model):
# #     text = models.TextField(max_length=500)
# #     author = models.ForeignKey('users.User', on_delete=models.CASCADE)
# #     ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     is_active = models.BooleanField(default=True)
# #
# #     class Meta:
# #         ordering = ['created_at']
from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/ads/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']