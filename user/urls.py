from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView,
    AdminDashboardView,
    DoctorDashboardView,
    CreatePatientView,
    LabDashboardView,
    HybridPredictionView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('doctor-dashboard/', DoctorDashboardView.as_view()),
    path('lab-dashboard/', LabDashboardView.as_view()),   # ✅ FIXED
    path('create-patient/', CreatePatientView.as_view()),
    path("hybrid-predict/", HybridPredictionView.as_view()),
]