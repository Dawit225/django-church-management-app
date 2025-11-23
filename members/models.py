from django.db import models

# Define gender choices for better data integrity
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

# Define choices for the confessor question
CONFESSOR_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),
]

class Member(models.Model):
    """
    Represents a registered member of the church.
    """
    # Personal Information
    full_name = models.CharField(max_length=200, help_text="The member's full legal name.")
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    
    # Contact Information
    email = models.EmailField(unique=True, help_text="Must be unique. Used for member login/contact.")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)

    # Church-Specific Information
    has_father_confessor = models.BooleanField(
        choices=CONFESSOR_CHOICES,
        default=False,
        verbose_name="Has a Father Confessor?"
    )

    # Tracking/Meta Fields (Best Practice)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    # --- Model Methods ---

    def __str__(self):
        """String representation of the object, used primarily by the Django Admin."""
        return self.full_name

    class Meta:
        """Options for the model."""
        ordering = ['full_name'] # Default ordering for querysets
        verbose_name = "Church Member"
        verbose_name_plural = "Church Members"