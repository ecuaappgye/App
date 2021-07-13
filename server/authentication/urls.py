from django.urls import path, include

from .apis import UserLogoutApi, UserPasswordReset, UserRegisterApi, UserLoginApi

authentication_urls = [
    path("register/", UserRegisterApi.as_view()),
    path("login/", UserLoginApi.as_view()),
    path("logout/", UserLogoutApi.as_view()),
    path("password_reset/", UserPasswordReset.as_view())
]

urlpatterns =[
    path("auth/", include((authentication_urls)))
]