from django import forms
from .models import Member

class MemberRegistrationForm(forms.ModelForm):
    """
    A form based on the Member model for public registration.
    """
    class Meta:
        model = Member
        # We specify the exact fields the user is allowed to submit
        fields = [
            'full_name', 
            'age', 
            'gender', 
            'email', 
            'phone_number', 
            'address', 
            'has_father_confessor'
        ]
        
        # Optional: Add user-friendly labels that override the model's verbose_name
        labels = {
            'has_father_confessor': 'Do you currently have a father confessor?',
        }
        
        # Optional: Add custom widgets for better UI control (e.g., for age input)
        widgets = {
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'address': forms.Textarea(attrs={'rows': 4}),
        }