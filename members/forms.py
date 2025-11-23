from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

# --- 1. Custom User Creation Form ---
class MemberUserCreationForm(UserCreationForm):
    """
    Extends Django's secure UserCreationForm to handle first_name and last_name.
    """
    # Adding extra fields that exist on the built-in User model but aren't in UserCreationForm by default
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)

    class Meta(UserCreationForm.Meta):
        # We inherit UserCreationForm's Meta but add first_name and last_name to the fields list
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
    # We must explicitly define the email field here because the base UserCreationForm doesn't enforce it.
    # The default User model's email field is not required, so we make it required here for registration.
    email = forms.EmailField(required=True) 

# --- 2. Member Profile Form ---
class MemberProfileForm(forms.ModelForm):
    """
    Form for the church-specific data linked via OneToOneField.
    """
    class Meta:
        model = Member
        # Only include the fields that now exist on the Member model (everything EXCEPT the User field)
        fields = ['age', 'gender', 'phone_number', 'address', 'has_father_confessor']
        
        labels = {
            'has_father_confessor': 'Do you currently have a father confessor?',
        }
        
        widgets = {
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'address': forms.Textarea(attrs={'rows': 4}),
        }