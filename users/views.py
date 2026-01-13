from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """CRUD for Users (requires authentication)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        """Users can only see their own profile unless they're admin."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """Get current user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def change_password(self, request):
        """Change password endpoint."""
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            # Regenerate token after password change for security
            Token.objects.filter(user=request.user).delete()
            token = Token.objects.create(user=request.user)

            return Response(
                {
                    "message": "Password changed successfully",
                    "token": token.key,  # Return new token
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def logout(self, request):
        """Logout by deleting the token."""
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(generics.CreateAPIView):
    """Register a new user (open to everyone)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Handle user registration with proper validation."""
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Get the token that was created in the serializer
            token = Token.objects.get(user=user)

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "token": token.key,
                    "message": "User registered successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Handle any validation errors
            return Response(
                {
                    "error": "Registration failed",
                    "details": (
                        serializer.errors if hasattr(serializer, "errors") else str(e)
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """Login with email or username and return auth token"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Login with email or username.
        Accepts: {"email": "user@example.com", "password": "pass"}
        or: {"username": "username", "password": "pass"}
        """
        # Check if using email or username
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not password:
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = None

        # Try to authenticate with email first
        if email:
            # Validate email format
            serializer = LoginSerializer(data={"email": email, "password": password})
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid email format", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Normalize email
            email = serializer.validated_data["email"]

            # Get user by email
            try:
                user_obj = User.objects.get(email=email)
                # Authenticate using username (Django's default)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        # Try username if email login failed or wasn't provided
        elif username:
            user = authenticate(username=username, password=password)

        else:
            return Response(
                {"error": "Email or username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if authentication was successful
        if user:
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """Logout by deleting auth token"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Delete the user's auth token."""
        try:
            # Delete the token
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Logout failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
