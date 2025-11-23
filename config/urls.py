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
# CRITICAL: TemplateView must be imported
from django.views.generic import TemplateView 

urlpatterns = [
    # Project-level Admin site
    path('admin/', admin.site.urls),
    
    # Include all URLs from the 'members' app under the path 'members/'
    path('members/', include('members.urls')),

    # 1. SUCCESS PAGE: The success_url defined in MemberRegistrationView resolves to this name.
    # We correctly use TemplateView.as_view(template_name=...) here.
    path('members/success/', 
         TemplateView.as_view(template_name='members/registration_success.html'), 
         name='registration_success'),

    # 2. HOME PAGE: A simple root path using TemplateView
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
]
