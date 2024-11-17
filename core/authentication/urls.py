from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


app_name = 'authentication'

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('refresh', TokenRefreshView.as_view(), name='refresh')
]