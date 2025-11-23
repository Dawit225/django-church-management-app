from django.urls import path
from .views import MemberRegistrationView, MemberDashboardView, MemberProfileUpdateView # Import new view

urlpatterns = [
    # Registration
    path('register/', MemberRegistrationView.as_view(), name='member_registration'),
    
    # Restricted Dashboard
    path('dashboard/', MemberDashboardView.as_view(), name='member_dashboard'),
    
    # Profile Update (Only one profile per user, so no PK needed)
    path('profile/edit/', MemberProfileUpdateView.as_view(), name='member_profile_update'), 
]