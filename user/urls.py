from django.urls import path
from .views import RegisterView
from .views import (
    ProfileView,
    LoginView,
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView,
    AdminDashboardView,
    DoctorDashboardView,
    CreatePatientView,
    LabDashboardView,
    HybridPredictionView,
    CreateSampleView,
    UpdateCollectionView,
    UpdateAdditionalDetailsView,
    RecordTestView,
    SampleDetailView,
    TestHistoryListView,
    UserListView,
    AntibioticsListView,
    ProfileUpdateView,
    UploadPlateImageView,
    UploadLabReportView,
    CreateTestView,
    ListTestsView,
    BacteriaListView
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('doctor-dashboard/', DoctorDashboardView.as_view()),
    path('lab-dashboard/', LabDashboardView.as_view()),   # ✅ FIXED
    path('create-patient/', CreatePatientView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    path("hybrid-prediction/", HybridPredictionView.as_view()),
    path("create-sample/", CreateSampleView.as_view()),
    path("update-collection/<int:pk>/", UpdateCollectionView.as_view()),
    path("update-additional-details/<int:pk>/", UpdateAdditionalDetailsView.as_view()),
    path("record-test/", RecordTestView.as_view()),
    path("update-plate-image/<int:pk>/", UploadPlateImageView.as_view()),
    path("update-lab-report/<int:pk>/", UploadLabReportView.as_view()),
    path("sample/<int:pk>/", SampleDetailView.as_view()),
    path("register-patient/", CreatePatientView.as_view(), name='register-patient'),
    path("register-patient", CreatePatientView.as_view()), # Without slash for safety
    path("auth/register-patient/", CreatePatientView.as_view()),
    path("test-history/", TestHistoryListView.as_view()),
    path("system-users/", UserListView.as_view()),
    path("auth/antibiotics/", AntibioticsListView.as_view()),

    # New paths from backend
    path('create-test/', CreateTestView.as_view(), name='create-test'),
    path('list-tests/', ListTestsView.as_view(), name='list-tests'),
    path('bacteria/', BacteriaListView.as_view(), name='bacteria-list'),
]