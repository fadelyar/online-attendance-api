from django.db import models
from django.utils import timezone
from user_profile.models import Profile


class Student(models.Model):
    name = models.CharField(max_length=300)
    father_name = models.CharField(max_length=300)
    email = models.EmailField(unique=True, default=None, null=True)
    profile_picture = models.URLField(default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    class_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    excel_sheet_path = models.CharField(max_length=300)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name
