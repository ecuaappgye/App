from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from server.api.mixins import ApiAuthMixin, ApiErrorsMixin
from server.users.selectors import user_data
from server.users.services import (user_create, user_email_change,
                                   user_password_change, user_password_reset,
                                   user_password_reset_check,
                                   user_update_profile, user_unique_session)


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
        
        user_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserLoginApi(APIView):
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response({"message":"Credenciales no válidas."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Eliminar sesión si ya existe el usuario.
        # Borrar la sesión de la base de datos.
        user_unique_session(user=user)

        login(request, user)
        data = user_data(user=user)

        return Response({
            "data":data,
            "session":request.session.session_key
        })


class UserLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_201_CREATED)


class UserUpdateProfile(ApiErrorsMixin, ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        password = serializers.CharField(required=False)
        avatar = serializers.ImageField(required=False)

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_update_profile(user_id=user_id, data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserPasswordReset(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
    
    def post(self, request):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_password_reset(**serializer.validated_data)

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






        
