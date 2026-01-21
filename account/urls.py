from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Включаем все стандартные URL-адреса аутентификации
    path('', include('django.contrib.auth.urls')),

    # Переопределяем только password_reset с кастомными шаблонами
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            html_email_template_name='registration/password_reset_email.html',
        ),
        name='password_reset'),

    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]