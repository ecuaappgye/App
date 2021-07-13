from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from server.users.services import user_create, user_update_profile
from server.users.selectors import user_data
from server.api.mixins import ApiErrorsMixin, ApiAuthMixin
from django.contrib.auth import authenticate, login, logout


class UserRegisterApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        email = serializers.EmailField()
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
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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


class UserUpdateProfile(APIView):
    
    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        password = serializers.CharField(required=False)

    def post(self, request, user_id):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_update_profile(user_id=user_id, data=serializer.validated_data)

        return  Response(status=status.HTTP_201_CREATED)




        
