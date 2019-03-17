from django.urls import path
from .views import StudentsView, QrCodesView


urlpatterns = [
    path('students/<int:pk>', StudentsView.as_view(), name='students_patch'),
    path('students/', StudentsView.as_view(), name='students_get'),
    path('qrcodes/<int:pk>', QrCodesView.as_view(), name='qrCodes'),
]
