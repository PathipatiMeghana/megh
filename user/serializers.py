from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Test

User = get_user_model()


# ================= REGISTER SERIALIZER =================
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data.get('role')
        )
        return user


# ================= PATIENT SERIALIZER =================
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['doctor']


# ================= TEST SERIALIZER =================
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'