from django.urls import path
from accounts import views



# Include your URL patterns here.
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('logout/', views.UserLogout.as_view(), name='logout'),
    # path('users/', views.UserList.as_view(), name='user_list'),
    # path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    # path('users/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    # path('users/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    # path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    # path('password-reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    # path('password-reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]