from django.urls import path
from .views import MemberRegistrationView, MemberDashboardView # Import new view

urlpatterns = [
    # Registration
    path('register/', MemberRegistrationView.as_view(), name='member_registration'),
    
    # Restricted Dashboard
    path('dashboard/', MemberDashboardView.as_view(), name='member_dashboard'),
]