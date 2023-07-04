from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=Roles.ADMIN,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Roles(models.TextChoices):
    USER = 'user', "USER"
    ADMIN = 'admin', "ADMIN"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(region='RU', max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices, default=Roles.USER)
    image = models.ImageField(upload_to='images/users_avatars/')
    is_active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN

    @property
    def is_user(self):
        return self.role == Roles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        ordering = ['id']
