from django.contrib import admin
from .models import Member

# Optional: Customize the admin list view for the Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # What fields to display in the change list view
    list_display = ('full_name', 'email', 'age', 'gender', 'has_father_confessor', 'date_joined')
    
    # Enable searching by these fields
    search_fields = ('full_name', 'email', 'phone_number')
    
    # Enable filtering by these fields
    list_filter = ('gender', 'has_father_confessor', 'date_joined')
    
    # Group fields in the detail view for better organization
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'age', 'gender', 'has_father_confessor')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone_number', 'address'),
            'classes': ('collapse',), # Optional: Collapse this section by default
        }),
    )

# Note: Using the @admin.register decorator is the modern best practice.