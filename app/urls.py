from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('login/', views.loginView, name='login'),
    path('signup/', views.signup, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('jobs/', views.jobView, name='jobs'),
    path('apply/', views.applyView, name='apply'),
    path('my-applied/',views.myAppliedJobView,name='my-applied'),
    path('internships/',views.internShipView,name='internships'),
    path('startups/',views.startupView,name='startups'),
]