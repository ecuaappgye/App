from django.urls import include, path

from .apis import (UserEmailChange, UserLoginApi, UserLogoutApi, UserPasswordChange,
                   UserPasswordReset, UserPasswordResetCheck, UserRegisterApi, UserUpdateProfile)

authentication_urls = [
    path("register/", UserRegisterApi.as_view()),
    path("login/", UserLoginApi.as_view()),
    path("logout/", UserLogoutApi.as_view()),
    path("update_profile/<int:user_id>/", UserUpdateProfile.as_view()),
    path("password_reset/", UserPasswordReset.as_view()),
    path("password_reset_check/", UserPasswordResetCheck.as_view()),
    path("password_change/<int:user_id>/", UserPasswordChange.as_view()),
    path("email_change/<int:user_id>/", UserEmailChange.as_view())
]

urlpatterns =[
    path("auth/", include((authentication_urls)))
]
