from django.db import models
from django.utils import timezone
from user_profile.models import Profile
import uuid


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)
    father_name = models.CharField(max_length=300, default=None)
    email = models.EmailField(unique=True, default=None, null=True)
    profile_picture = models.URLField(default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    class_name = models.CharField(max_length=300)
    short_description = models.CharField(max_length=500, default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.class_name
