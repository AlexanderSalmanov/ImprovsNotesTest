import redis
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers import UserSerializer


redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])


class SignupView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        operation_summary="POST request",
        operation_description="User signup endpoint",
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Successful registration",
                schema=UserSerializer,
                examples={
                    "username": "myName",
                    "email": "myemail@mail.com",
                    "password": "myPassword"
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data submission")
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('access')
        redis_client.set(f'jwt:{token}', '', ex=60*60)

        return response
    
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    @swagger_auto_schema(
        operation_summary="Logout view",
        operation_description="Logout current user",
        responses={
            status.HTTP_200_OK: openapi.Response(description="Successful operation")
        }
    )
    def post(self, request, *args, **kwargs):
        token = request.auth
        if token:
            redis_client.delete(f'jwt:{token}')
        return Response(status=status.HTTP_200_OK)