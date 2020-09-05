from django.urls import path
from jwt_auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token/', views.ObtainTokenView.as_view(), name='obtain_token'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh_token')
]