from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .services.ml_engine import ml_predict
from .services.statistical_engine import statistical_probability
import random

from .serializers import (
    RegisterSerializer,
    PatientSerializer,
    TestSerializer,
)
from .permissions import IsAdminRole, IsDoctor,IsLabRole
from .models import Patient, Test, Bacteria, Antibiotic


User = get_user_model()
# ================= HYBRID PREDICTION =================
class HybridPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            age = int(request.GET.get("age"))
            gender = request.GET.get("gender")
            bacteria = request.GET.get("bacteria")
            antibiotic = request.GET.get("antibiotic")

            bacteria_obj = Bacteria.objects.get(name=bacteria)
            antibiotic_obj = Antibiotic.objects.get(name=antibiotic)

            ml_prob = ml_predict(
                age,
                gender,
                bacteria_obj.id,
                antibiotic_obj.id
            )

            stat_prob = statistical_probability(
                bacteria,
                antibiotic
            )

            final_prob = (0.6 * ml_prob) + (0.4 * stat_prob)

            prediction = "Resistant" if final_prob > 0.5 else "Susceptible"

            return Response({
                "ml_probability": round(ml_prob, 3),
                "statistical_probability": round(stat_prob, 3),
                "final_probability": round(final_prob, 3),
                "prediction": prediction
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# ================= ADMIN DASHBOARD =================
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        total_users = User.objects.count()
        total_tests = Test.objects.count()
        total_bacteria = Bacteria.objects.count()
        total_antibiotics = Antibiotic.objects.count()

        one_week_ago = timezone.now() - timedelta(days=7)
        this_week_tests = Test.objects.filter(
            created_at__gte=one_week_ago
        ).count()

        recent_tests = Test.objects.all().order_by('-created_at')[:5]

        recent_data = [
            {
                "id": test.id,
                "bacteria_name": test.bacteria_name,
                "doctor": test.doctor.username,
                "created_at": test.created_at
            }
            for test in recent_tests
        ]

        return Response({
            "admin": request.user.username,
            "total_users": total_users,
            "total_tests": total_tests,
            "this_week_tests": this_week_tests,
            "total_bacteria": total_bacteria,
            "total_antibiotics": total_antibiotics,
            "recent_tests": recent_data
        })


# ================= DOCTOR DASHBOARD =================
class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor = request.user

        total_tests = Test.objects.filter(doctor=doctor).count()

        one_week_ago = timezone.now() - timedelta(days=7)
        this_week_tests = Test.objects.filter(
            doctor=doctor,
            created_at__gte=one_week_ago
        ).count()

        return Response({
            "doctor": doctor.username,
            "total_tests": total_tests,
            "this_week_tests": this_week_tests
        })
    # ================= LAB DASHBOARD =================
class LabDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsLabRole]

    def get(self, request):
        total_tests = Test.objects.count()

        one_week_ago = timezone.now() - timedelta(days=7)
        this_week_tests = Test.objects.filter(
            created_at__gte=one_week_ago
        ).count()

        return Response({
            "lab": request.user.username,
            "total_tests": total_tests,
            "this_week_tests": this_week_tests
        })


# ================= CREATE PATIENT =================
class CreatePatientView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ================= REGISTER =================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)

        return Response(serializer.errors, status=400)


# ================= LOGIN =================
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role,   # ✅ Directly use role field
            "username": user.username
        })

# ================= FORGOT PASSWORD =================
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email required"}, status=400)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_verified = False
        user.save()

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent successfully"})


# ================= VERIFY OTP =================
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        if user.otp != otp:
            return Response({"error": "Invalid OTP"}, status=400)

        user.otp_verified = True
        user.save()

        return Response({"message": "OTP verified successfully"})


# ================= RESET PASSWORD =================
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        if not user.otp_verified:
            return Response({"error": "OTP not verified"}, status=400)

        user.set_password(new_password)
        user.otp = None
        user.otp_verified = False
        user.save()

        return Response({"message": "Password reset successful"})
    
    