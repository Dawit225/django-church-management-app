"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# Import the built-in LogoutView
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    # Project-level Admin site
    path('admin/', admin.site.urls),
    
    # 1. EXPLICIT LOGOUT DEFINITION (FIX)
    # Define the logout URL explicitly using the correct name 'logout'
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    
    # CORE AUTHENTICATION PATHS (This include will handle all others like login, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Member App Paths
    path('members/', include('members.urls')),

    # Success/Home Paths
    path('members/success/', 
         TemplateView.as_view(template_name='members/registration_success.html'), 
         name='registration_success'),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
]
