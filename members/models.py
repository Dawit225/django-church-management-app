from django.db import models
# Import the User model that Django uses for authentication
from django.contrib.auth.models import User 

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

CONFESSOR_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),
]

class Member(models.Model):
    """
    Holds church-specific profile data, linked to one Django User for login/security.
    """
    # CRITICAL: One-to-One Link to the User Account
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # Why CASCADE? If the User account is deleted, their Member profile is also deleted.
    
    # Personal Information (fields that are specific to the church context)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    
    # Contact Information (We removed 'email' as the User model handles it)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)

    # Church-Specific Information
    has_father_confessor = models.BooleanField(
        choices=CONFESSOR_CHOICES,
        default=False,
        verbose_name="Has a Father Confessor?"
    )

    # Tracking/Meta Fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    # --- Model Methods ---

    def __str__(self):
        """Uses the linked User's username/email for a clear string representation."""
        return f"Member: {self.user.username} ({self.user.email})"

    class Meta:
        # ... (ordering and verbose_name can remain the same)
        pass