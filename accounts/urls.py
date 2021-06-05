from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('addJobs/', views.addJobs, name="addJobs"),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    path('how_work/', views.how_work, name="how_work"),
    path('coming_soon/', views.coming_soon, name="coming_soon"),
    path('view_proposal/<str:job_id>/<str:proposal_id>/', views.view_proposal, name="view_proposal"),
    path('message/<str:job_id>/<str:proposal_id>/', views.message, name="message"),
    path('freelancer_proposal/', views.freelancer_proposal, name="freelancer_proposal"),
    path('jobs/', views.jobs, name="jobs"),
    path('about/', views.about, name="about"),
    path('add_proposal/<str:job_id>/', views.add_proposal, name="add_proposal"),
    path('manage_jobs/', views.manage_jobs, name="manage_jobs"),
    path('job_single/<str:pk>/', views.job_single, name="job_single"),
    path('job_proposal/<str:job_id>/', views.job_proposal, name="job_proposal"),
    path('job_completed/<str:job_id>/', views.job_completed, name="job_completed"),
    path('view_freelancers/', views.view_freelancers, name="view_freelancers"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('user_account/', views.user_account, name="user_account"),
    path('addSkills/<str:pk>/', views.addSkills, name="addSkills"),
    path('addExperience/<str:pk>/', views.addExperience, name="addExperience"),
    path('addEducation/<str:pk>/', views.addEducation, name="addEducation"),
    path('addProject/<str:pk>/', views.addProject, name="addProject"),
    path('addAward/<str:pk>/', views.addAward, name="addAward"),
    path('freelancer/<str:pk>/', views.freelancer, name="freelancer"),
    

    path('checkout/<str:job_id>/<str:winner_id>/', views.checkout, name='checkout'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('paypal_complete/', views.paypal_complete, name='paypal_complete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]