from django.urls import include, path

from .apis import (UserEmailChange, UserGetApi, UserLoginApi, UserLogoutApi,
                   UserPasswordChange, UserPasswordReset,
                   UserPasswordResetCheck, UserRegisterApi,
                   UserRegisterVerifyApi, UserRegisterVerifyCheckApi,
                   UserUpdateApi)

authentication_urls = [
    path('get/<int:user_id>/', UserGetApi.as_view(), name='get'),

    path('register/', UserRegisterApi.as_view()),
    path('register/verify/<int:user_id>/', UserRegisterVerifyApi.as_view()),
    path('register/verify_check/<int:user_id>/', UserRegisterVerifyCheckApi.as_view()),

    path('login/', UserLoginApi.as_view(), name='login'),
    path('logout/', UserLogoutApi.as_view(), name='logout'),

    path('password_reset/', UserPasswordReset.as_view()),
    path('password_reset_check/', UserPasswordResetCheck.as_view()),
    path('password_change/<int:user_id>/', UserPasswordChange.as_view(), name='password_change'),

    path('email_change/<int:user_id>/', UserEmailChange.as_view(), name='email_change')
]

drivers_urls =[
    path('update/<int:user_id>/', UserUpdateApi.as_view(), name='update')
]

urlpatterns =[
    path('auth/', include((authentication_urls, 'auth'))),
    path('driver/', include((drivers_urls, 'driver')))
]
