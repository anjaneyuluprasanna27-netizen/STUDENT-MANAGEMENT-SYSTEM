from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    COURSE_CHOICES = [
        ('BCA', 'BCA'),
        ('BSC_CS', 'B.Sc Computer Science'),
        ('BTECH_CSE', 'B.Tech CSE'),
        ('MCA', 'MCA'),
        ('MSC_IT', 'M.Sc IT'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.roll_number})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def email(self):
        return self.user.email
