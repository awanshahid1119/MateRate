from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'authentication'

urlpatterns = [
    path('', views.welcome_page, name="Welcome page"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.user_register, name='signup'),
    path('user/validate/', views.isValid_User, name='validate user'),
    path('logout/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='logout'),
    path('student/profile/', views.StudentView.as_view(), name='profile'),
    path('account/update/username/',
         views.ChangeUsernameView.as_view(), name='change_username'),
    path('account/update/password/',
         views.ChangePasswordView.as_view(), name='change_password'),

    path('registration/', views.UserStudentRegistration,
         name="UserStudentRegistration"),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request_reset_email"),

    path('password_reset_complete/', views.SetNewPasswordAPIView,
         name="password_reset_complete"),
    path('checkOTP/', views.CheckOTP, name="checkOTP"),
    path('student/studentprofile/', views.studentprofile, name='studentprofile'),
    path('student/savestudentprofile/',
         views.savestudentprofile, name='studentprofile'),
    path('student/change/password/', views.changeProfilePassword,
         name='change_profile_password'),
]