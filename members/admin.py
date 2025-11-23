from django.contrib import admin
from .models import Member
from .models import Member, Announcement, VideoContent # Import new models

# Optional: Customize the admin list view for the Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    
    # 1. NEW list_display: Use custom methods (defined below) and fields that exist on Member
    list_display = ('get_full_name', 'get_email', 'age', 'gender', 'has_father_confessor', 'date_joined')
    
    # 2. NEW search_fields: Can only search on fields directly on the Member model, 
    # or fields accessible through the __ (double underscore) relationship operator.
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number')
    
    # 3. list_filter remains the same
    list_filter = ('gender', 'has_father_confessor', 'date_joined')
    
    # 4. fieldsets: We need to include the 'user' field for linking and remove the old fields
    fieldsets = (
        ('Authentication Link', {
            'fields': ('user',), # CRITICAL: Admin must be able to link to a User
        }),
        ('Church Profile Info', {
            'fields': ('age', 'gender', 'has_father_confessor'),
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'address'),
            'classes': ('collapse',),
        }),
    )

    # --- Custom Methods to Display User Fields ---
    
    def get_full_name(self, obj):
        """Displays the full name from the linked User object."""
        return obj.user.get_full_name()
    # Optional: sets the column header name in the Admin List View
    get_full_name.short_description = 'Full Name' 
    
    def get_email(self, obj):
        """Displays the email from the linked User object."""
        return obj.user.email
    get_email.short_description = 'Email Address'

# Note: We removed 'full_name' and 'email' from the Admin configuration
# and replaced them with the method calls 'get_full_name' and 'get_email'.

# 1. Admin for Announcements
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_event', 'event_date', 'posted_by', 'created_at')
    list_filter = ('is_event', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at' # Add drill-down navigation by date
    
    # Automatically set posted_by to the currently logged-in admin user
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only set on creation
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)

# 2. Admin for Video Content
@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'posted_by', 'created_at')
    search_fields = ('title', 'description')
    
    # Use fieldsets to organize the display
    fieldsets = (
        (None, {
            'fields': ('title', 'youtube_url', 'description')
        }),
        ('Metadata', {
            'fields': ('posted_by',),
            'classes': ('collapse',),
        })
    )
    
    # Automatically set posted_by
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)