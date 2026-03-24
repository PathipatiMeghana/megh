from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Test, TestRecord, SecurityLog, Sample, Bacteria, Antibiotic

User = get_user_model()


# REGISTER
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'phone', 'hospital', 'experience_years']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


# PATIENT
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ['doctor']

# SAMPLE
class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"

# TEST
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


# TEST RECORD
class RecordTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRecord
        fields = "__all__"

class TestRecordDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    sample_type = serializers.CharField(source='sample.sample_type', read_only=True)
    
    class Meta:
        model = TestRecord
        fields = ['id', 'patient', 'patient_name', 'sample', 'sample_type', 'bacteria', 'antibiotic', 'prediction', 'timestamp', 'is_correct']


# SECURITY LOG
class SecurityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityLog
        fields = "__all__"

# BACTERIA
class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = "__all__"

# ANTIBIOTIC
class AntibioticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antibiotic
        fields = "__all__"