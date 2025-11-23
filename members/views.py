from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView # New import for handling multiple forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, UpdateView # Added UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Added UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404 # Added get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from .models import Member, Announcement, VideoContent
from django.urls import reverse_lazy
# FIX: Ensure ListView is imported here:
from django.views.generic import TemplateView, View, ListView 
from django.views.generic.edit import FormView, UpdateView

from .models import Member
from .forms import MemberUserCreationForm, MemberProfileForm # Import the new forms

# We'll use a custom View to handle the two forms in one page.

class MemberRegistrationView(View):
    """
    Handles displaying and processing the User creation (login details) 
    and Member profile creation (church details) simultaneously.
    """
    user_form = MemberUserCreationForm
    profile_form = MemberProfileForm
    template_name = 'members/member_registration.html'
    success_url = reverse_lazy('registration_success')

    def get(self, request, *args, **kwargs):
        """Handle GET request: display empty forms."""
        context = {
            'user_form': self.user_form(),
            'profile_form': self.profile_form(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle POST request: validate and save both forms."""
        user_form = self.user_form(request.POST)
        profile_form = self.profile_form(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # 1. Save the User Form first
            new_user = user_form.save()
            
            # 2. Save the Member Form, linking the new_user via OneToOneField
            member_profile = profile_form.save(commit=False)
            member_profile.user = new_user  # CRITICAL: Establish the One-to-One link
            member_profile.save()

            # Optional: Log the user in immediately after registration (best practice for UX)
            # from django.contrib.auth import login
            # login(request, new_user)
            
            return redirect(self.success_url)
        
        # If either form is invalid, re-render the page with errors
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

class MemberDashboardView(LoginRequiredMixin, TemplateView):
    """
    A simple view for logged-in members.
    The LoginRequiredMixin ensures that only authenticated users can access this page.
    """
    template_name = 'members/member_dashboard.html'
    
    # If the user is not logged in, they will be redirected to the URL defined by settings.LOGIN_URL
    # which is configured to 'login'.

class MemberProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows a logged-in user to update their associated Member profile data.
    """
    model = Member
    form_class = MemberProfileForm # Reuse the form we defined for profile data
    template_name = 'members/member_profile_update.html'
    
    # URL to redirect to after successful update (dashboard is a good choice)
    success_url = reverse_lazy('member_dashboard')

    # CRITICAL: Security Check 1 - Ensure the user only edits THEIR profile
    def get_object(self, queryset=None):
        """
        Tries to return the Member object linked to the current user.
        If not found, it raises a 404, or we can handle the redirect here.
        """
        try:
            # We use .get() here instead of get_object_or_404 to explicitly handle the exception
            return Member.objects.get(user=self.request.user)
        except Member.DoesNotExist:
            # OPTIONAL GRACEFUL HANDLING:
            # Instead of allowing the 404 to be raised, you could redirect
            # the user to a page that prompts them to create a profile.
            # For now, we'll stick to the original logic which raises 404 
            # (which is what get_object_or_404 did, just explicitly now).
            raise Http404("No Member profile found for the logged-in user.")

    # CRITICAL: Security Check 2 - UserPassesTestMixin requires this method.
    def test_func(self):
        """
        Tests if the logged-in user (self.request.user) is the owner of the object.
        This is technically redundant because of get_object(), but it's a solid defense layer.
        """
        return self.get_object().user == self.request.user
    
class AnnouncementListView(LoginRequiredMixin, ListView):
    """Displays a list of all church announcements."""
    model = Announcement
    template_name = 'members/announcement_list.html'
    context_object_name = 'announcements' # The variable name to use in the template
    paginate_by = 10 # Optional: Show 10 announcements per page


class VideoContentListView(LoginRequiredMixin, ListView):
    """Displays a list of all church video content."""
    model = VideoContent
    template_name = 'members/video_list.html'
    context_object_name = 'videos' # The variable name to use in the template
    paginate_by = 9 # Display a grid of 9 videos