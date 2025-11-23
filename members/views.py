from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Member
from .forms import MemberRegistrationForm

class MemberRegistrationView(CreateView):
    """
    Handles displaying and processing the new member registration form.
    Uses Django's built-in CreateView CBV.
    """
    model = Member
    form_class = MemberRegistrationForm # Use our custom form
    template_name = 'members/member_registration.html'
    
    # Where to redirect the user after a successful form submission
    success_url = reverse_lazy('registration_success') 
    
    # Note on reverse_lazy: It is preferred over reverse() in class attributes 
    # because it resolves the URL lazily (after the app's URL configuration is fully loaded).