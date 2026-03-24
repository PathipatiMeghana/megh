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
    phone = models.CharField(max_length=15, blank=True, null=True)
    hospital = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.FloatField(default=0)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ================= TEST RECORD =================
class TestRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, null=True, blank=True)
    bacteria = models.CharField(max_length=200)
    antibiotic = models.CharField(max_length=200)
    prediction = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bacteria} - {self.antibiotic}"


# ================= SECURITY LOG =================
class SecurityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action


# ================= PATIENT =================
class Patient(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    patient_id = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= TEST =================
class Test(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bacteria_name = models.CharField(max_length=100)
    antibiotic_name = models.CharField(max_length=100, default='Unknown')
    result = models.CharField(max_length=10, choices=[('R', 'Resistant'), ('S', 'Sensitive'), ('I', 'Intermediate')], default='S')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bacteria_name


# ================= BACTERIA =================
class Bacteria(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ================= SAMPLE =================
class Sample(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    sample_type = models.CharField(max_length=100)
    sample_id = models.CharField(max_length=100)
    plate_image = models.ImageField(upload_to="samples/plates/", null=True, blank=True)
    lab_report = models.FileField(upload_to="samples/reports/", null=True, blank=True)
    
    collection_date = models.CharField(max_length=50, null=True, blank=True)
    collection_time = models.CharField(max_length=50, null=True, blank=True)
    collection_site = models.CharField(max_length=100, null=True, blank=True)
    collected_by = models.CharField(max_length=100, null=True, blank=True)
    
    sample_volume = models.CharField(max_length=100, null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sample_type} - {self.sample_id}"

# ================= ANTIBIOTIC =================
class Antibiotic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name