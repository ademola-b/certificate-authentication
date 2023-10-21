from django.urls import path
from . views import (HomePageView, LoginView, LogoutView,
                     DashboardView, 
                     GenerateCertificateView, AuthenticateCertificateView, 
                     ScannerView, ScannedResultView)
app_name = 'auth'
urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('generate-certificate/', GenerateCertificateView.as_view(), name='generate_certificate'),
    path('authenticate-certificate/', AuthenticateCertificateView.as_view(), name='authenticate_certificate'),
    path('scanner/', ScannerView.as_view(), name='scanner_view'),
    path('authenticate-certificate/scanned-result/<str:content>/', ScannedResultView.as_view(), name='scanned_result'),
]
