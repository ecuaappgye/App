import email
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from server.api.mixins import ApiAuthMixin, ApiErrorsMixin
from server.users.selectors import user_by_email, user_by_id, user_data
from server.users.services import (user_account_active, user_create,
                                   user_email_change, user_password_change,
                                   user_password_reset,
                                   user_password_reset_check,
                                   user_unique_session, user_update_profile)

from .services import user_create_verify, user_create_verify_check


class UserRegisterApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        avatar = serializers.ImageField(default=None)
        password = serializers.CharField()

    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)

        return Response({'user_id': user.id, 'is_active':user.is_active},
                        status=status.HTTP_201_CREATED)


class UserRegisterVerifyApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15)

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_create_verify(user_id=user_id,
                           user_agent= request.META.get('HTTP_USER_AGENT'),
                           ip_address= request.META.get('REMOTE_ADDR'),
                           **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserRegisterVerifyCheckApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_create_verify_check(user_id=user_id, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserUpdateApi(ApiErrorsMixin, ApiAuthMixin, APIView):
    class Inputerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        address = serializers.CharField()
        phone = serializers.CharField()
        cdi = serializers.CharField()

    def post(self, request, user_id):
        serializer = self.Inputerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_update_profile(user_id=user_id, data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserLoginApi(APIView):
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if user_account_active(email=email) is False:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = authenticate(request, **serializer.validated_data)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        session = user_unique_session(user=user)
        if session is not None:
            return Response(status=status.HTTP_409_CONFLICT)

        login(request, user)
        data = user_data(user=user)

        return Response({"data": data,"session": request.session.session_key})


class UserLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_201_CREATED)


class UserPasswordReset(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_reset(user_agent= request.META.get('HTTP_USER_AGENT'),
                            ip_address= request.META.get('REMOTE_ADDR'),
                            **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserPasswordResetCheck(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField()
        new_password = serializers.CharField()
        password_confirm = serializers.CharField()

    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_reset_check(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserPasswordChange(ApiErrorsMixin, ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        old_password = serializers.CharField()
        new_password = serializers.CharField()
        password_confirm = serializers.CharField()

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_change(user_id=user_id, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserEmailChange(ApiErrorsMixin, ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email_change(user_id=user_id, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserGetApi(ApiErrorsMixin, ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
        cdi = serializers.CharField()
        phone = serializers.CharField()
        address = serializers.CharField()

    def get(self, request, user_id):

        user = user_by_id(id=user_id)
        data = self.OutputSerializer(user).data

        return Response(data)
