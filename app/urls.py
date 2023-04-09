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
    path('my-profile/',views.myProfileView,name='my-profile'),
    path('post-job/',views.postJobView,name='post-job'),
    path('user-profile/<int:id>',views.viewUserProfileView,name='user-profile'),
    path('update-job/<int:id>',views.jobUpdateView,name='update-job'),
    path('delete-job/<int:id>',views.jobDeleteView,name='delete-job'),
    path('manage-jobs/',views.JobApplicationView,name='manage-jobs'),
    path('job-applications/<int:id>',views.jobApplicantsView,name='job-applicants'),
    path('create-company/',views.createCompanyProfile,name='create-company'),
    path('update-company/',views.updateCompanyProfile,name='update-company'),
    path('job-search/',views.searchJobs,name='job-search'),
    path('add_skill/',views.addSkillView,name='add_skill'),
    path('add-profile/',views.createProfileView,name='add-profile'),
    path('create-startup/',views.createStartup,name='create-startup'),
    path('update-startup/',views.updateStartup,name='update-startup'),
    path('join-startup/<int:id>/',views.joinStartupView,name='join-startup'),
    path('approve-team/<int:id>/',views.approveJoinStartup,name='approve-team'),
    path('careers/',views.careerInfoViewRIASEC,name='careers'),
    path('career-test/',views.careerTestView,name='career-test'),
    path('approve-candidate/<int:id>/',views.approveCandidate,name='approve-candidate'),
    path('interview-candidate/<int:id>',views.interviewCandidate,name='interview-candidate'),
    path('reject-candidate/<int:id>',views.rejectCandidate,name='reject-candidate'),


] 