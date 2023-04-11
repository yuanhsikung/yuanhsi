from django.urls import path
from . import views

urlpatterns = [
    path('查詢/', views.查詢, name='查詢'),
    path('birthday/', views.birthday, name='birthday'),
   
]

