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


class Announcement(models.Model):
    """
    Church announcements, events, and important messages.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Detailed message, including event details or fasting schedules.")
    is_event = models.BooleanField(default=False, verbose_name="Is this an event?")
    event_date = models.DateTimeField(null=True, blank=True)
    
    # Who created the announcement (Best Practice: link content to the User who posted it)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements') 
    # Use SET_NULL so if the admin user is deleted, the announcement remains.
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] # Display newest announcements first
        verbose_name_plural = "Announcements"

class VideoContent(models.Model):
    """
    Stores YouTube video links for embedding.
    """
    title = models.CharField(max_length=255)
    # The URL should be the full YouTube URL, e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ
    youtube_url = models.URLField(max_length=2000) 
    description = models.TextField(blank=True)
    
    # Metadata
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Video Content"

    # Custom method to extract the embed ID (CRITICAL for safe embedding)
    def get_youtube_embed_id(self):
        """
        Extracts the 'v=' parameter from the YouTube URL.
        Example: https://www.youtube.com/watch?v=VIDEO_ID -> VIDEO_ID
        """
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.youtube_url)
        # We need the 'v' parameter from the query string
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        return None