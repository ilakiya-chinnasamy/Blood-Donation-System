from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Existing LifeLink pages
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register_donor'),
    path('donors/', views.donor_list, name='donor_list'),

    path(
        'request-blood/',
        views.request_blood,
        name='request_blood'
    ),

    path('alerts/', views.alerts, name='alerts'),

    path(
        'alerts/<int:alert_id>/read/',
        views.mark_alert_read,
        name='mark_alert_read'
    ),

    # Login and logout
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='donors/login.html',
            redirect_authenticated_user=True,
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Forgot-password flow
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='donors/password_reset_form.html',
            email_template_name='donors/password_reset_email.html',
            subject_template_name='donors/password_reset_subject.txt',
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='donors/password_reset_done.html',
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='donors/password_reset_confirm.html',
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='donors/password_reset_complete.html',
        ),
        name='password_reset_complete'
    ),
]