from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreatePatientView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/register-patient/', CreatePatientView.as_view()),
    path('api/register-patient', CreatePatientView.as_view()), # Safety
    path('api/auth/register-patient/', CreatePatientView.as_view()), # For frontend_web consistency
    path('register-patient/', CreatePatientView.as_view()), # For root access
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)