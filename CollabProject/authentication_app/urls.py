from django.urls import path,include
from .views import LandingTemplateView, CustomLoginView, SignUpView, ActivateAccount, DashboardTemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', LandingTemplateView.as_view(), name="landingpage"),
    path('dashboard/', DashboardTemplateView.as_view(), name="dashboard"),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('activate_account/<uidb64>/<token>/',ActivateAccount.as_view(),name="activate_account"),
    path('login/', CustomLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset.html"), name='password_reset'), 

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="auth/password_reset_email.html"
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="auth/reset_completed.html"
    ), name='password_reset_complete'),
]
    

