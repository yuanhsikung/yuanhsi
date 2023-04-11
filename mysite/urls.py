"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from wbc2023 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn, name='signIn'),
    path('postsignIn/', views.postsignIn, name='postsignIn'),
    path('signUp/', views.signUp, name='signUp'),
    path('postsignUp/', views.postsignUp, name='postsignUp'),
    path('logout/', views.logout, name='logout'),
    path('validate/', views.validate, name='validate'),
    path('birthdaysave/', views.birthdaysave, name='birthdaysave'),
    path('words82/', views.words82, name='words82'),
    path('inquire/', views.inquire, name='inquire'),
    path('modifydatas/', views.modifydatas, name='modifydatas'),
    path('modifysave/', views.modifysave, name='modifysave'),
    path('postReset/', views.postReset, name='postReset'),
    path('table/', views.table, name='table'),
    path('home/', views.home, name='home'),




]
