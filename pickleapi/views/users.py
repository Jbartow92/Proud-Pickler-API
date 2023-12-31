from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from pickleapi.models import PickleUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}


class PickleUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PickleUser
        fields = ("user", "profile_image_url", "bio")


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

        
    @action(detail=False, methods=["get"], url_path="profile")
    def retrieve_user_profile(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the authenticated user
        user = request.user

        # Serialize the user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=False, methods=["get"], url_path="allusers")
    def list_all_users(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get all users
        users = User.objects.all()

        # Serialize the user data
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["put"], url_path="update")
    def update_user_profile(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the authenticated user
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Update user data
            serializer.save()

            # Update the user's password if provided
            password = request.data.get("password")
            if password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user session authenticated

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["get"], url_path="pickleusers")
    def get_pickle_users(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Filter PickleUser objects for the current authenticated user
        pickle_user = PickleUser.objects.filter(user=request.user).first()

        # Check if the PickleUser exists
        if pickle_user:
            serializer = PickleUserSerializer(pickle_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "PickleUser not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["put"], url_path="pickleuser/update")
    def update_pickle_user_profile(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the authenticated user's PickleUser
        pickle_user = PickleUser.objects.filter(user=request.user).first()
        if not pickle_user:
            return Response({"error": "PickleUser not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PickleUserSerializer(pickle_user, data=request.data, partial=True)

        if serializer.is_valid():
            # Update PickleUser data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["username"],
            )
            # Create or update PickleUser associated with the user
            pickle_user, created = PickleUser.objects.get_or_create(user=user)
            pickle_user.profile_image_url = request.data.get("profile_image_url")
            pickle_user.bio = request.data.get("bio")
            pickle_user.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
