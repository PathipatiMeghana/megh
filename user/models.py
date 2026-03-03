from django.contrib.auth.models import AbstractUser
from django.db import models


# ================= CUSTOM USER =================
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('lab', 'Lab'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True, blank=True)


# ================= PATIENT MODEL =================
class Patient(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= TEST MODEL =================
class Test(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bacteria_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bacteria_name


# ================= BACTERIA MODEL =================
class Bacteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# ================= ANTIBIOTIC MODEL =================
class Antibiotic(models.Model):
    name = models.CharField(max_length=100)
    effectiveness = models.CharField(max_length=50)

    def __str__(self):
        return self.name
   