from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.CustomUserRegisterView.as_view(), name='custom_register'),
        path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),
        path('token/refresh/', views.MyTokenRefreshView.as_view(), name='refresh'),
        path('user/update/', views.CustomUserUpdateView.as_view(), name='user_update'),
        path('user/password/change/', views.PasswordChangeView.as_view(), name='password_change'),
]