from django.contrib import admin
from .models import Member

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