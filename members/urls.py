from django.urls import path
# Import the new views
from .views import (
    MemberRegistrationView, 
    MemberDashboardView, 
    MemberProfileUpdateView, 
    AnnouncementListView, 
    VideoContentListView # NEW
)

urlpatterns = [
    # Registration & Profile
    path('register/', MemberRegistrationView.as_view(), name='member_registration'),
    path('dashboard/', MemberDashboardView.as_view(), name='member_dashboard'),
    path('profile/edit/', MemberProfileUpdateView.as_view(), name='member_profile_update'), 
    
    # --- CONTENT PATHS (NEW) ---
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('videos/', VideoContentListView.as_view(), name='video_list'),
]