from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    faculty = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'faculty'})
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    marks = models.IntegerField()
    
    class Meta:
        unique_together = ('student', 'subject')
        
    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}: {self.marks}"
