from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from . serializers import CustomUserRegisterSerializer, MyTokenObtainPairSerializer, PasswordChangeSerializer, CustomUserUpdateSerializer
from . models import RefreshTokenModels, CustomUser

from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserRegisterView(generics.CreateAPIView):
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [AllowAny]


    # def perform_create(self, serializer):
    #     user = serializer.save(user=self.request.user)
    #     response_serializer = ApartmentCreateSerializers(apartment)
    #     return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
                response_data = {
                    "data": [data],
                    "status": status.HTTP_200_OK,
                    "statusText": "Ok"
                }

                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'Login error: {e}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_headers = request.headers.get('Authorization')
            if auth_headers is None:
                return Response({'error': 'Authorization headers missing'}, status=status.HTTP_400_BAD_REQUEST)
            access_token = auth_headers.split(' ')[1]
            print(f'access token {access_token}')
            print(f'user {request.user}')

            user = request.user
            refresh_token_instances = RefreshTokenModels.objects.filter(user=user)
            for refresh_token_instance in refresh_token_instances:
                refresh_token = refresh_token_instance.token
                token = RefreshToken(refresh_token)
                token.blacklist()
                refresh_token_instance.delete()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except RefreshTokenModels.DoesNotExist:
            return Response({'error': 'Refresh tokrn dont found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class Refresh(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = request.data.get('token')
            refresh = RefreshToken(token)
            data = {
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



class CustomUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)