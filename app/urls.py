from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('login/', views.loginView, name='login'),
    path('signup/', views.signup, name='register'),
]