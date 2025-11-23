from django.urls import path
from .views import MemberRegistrationView

urlpatterns = [
    # URL for the registration form
    path('register/', MemberRegistrationView.as_view(), name='member_registration'),
    
    # We will remove the success path definition from here and keep it in config/urls.py 
    # since MemberRegistrationView's success_url is defined globally.
]