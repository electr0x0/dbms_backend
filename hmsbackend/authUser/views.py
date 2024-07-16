from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, UserDetailSerializer
from rest_framework.views import APIView

class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        if user_data:
            headers = self.get_success_headers(serializer.data)
            return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "User creation failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            session_token = serializer.create_session(user)
            
            user_detail_serializer = UserDetailSerializer(user)
            user_details = user_detail_serializer.data
            user_details['session_token'] = session_token
            
            response = Response(user_details, status=status.HTTP_200_OK)
            response.set_cookie('session_token', session_token, httponly=True)
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
