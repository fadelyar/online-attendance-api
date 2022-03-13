from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils import timezone
import uuid


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        # if not email:
        #     raise ValueError('email is required!')
        if len(password) < 5:
            raise ValueError('to short for password!')
        if len(password) > 20:
            raise ValueError('to long for password!')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    objects = UserManager()
    user_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default='', null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.CharField(max_length=255, default='', null=True)
    USERNAME_FIELD = 'user_name'

    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name
