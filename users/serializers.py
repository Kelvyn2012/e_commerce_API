from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=6
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def validate_email(self, value):
        """Validate email format and uniqueness."""
        if not value:
            raise serializers.ValidationError("Email is required.")

        value = value.lower().strip()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate_username(self, value):
        """Validate username uniqueness and format."""
        if not value:
            raise serializers.ValidationError("Username is required.")

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )

        # Try Django validators but don't fail for demo
        try:
            validate_password(value)
        except DjangoValidationError as e:
            # Log warning but allow for demo purposes
            print(f"Password validation warning: {e}")

        return value

    def create(self, validated_data):
        """Create user with validated data."""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login with email validation."""

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate(self, data):
        """Ensure either email or username is provided."""
        if not data.get("email") and not data.get("username"):
            raise serializers.ValidationError("Email or username is required.")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""

    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        """Validate email uniqueness (excluding current user)."""
        value = value.lower().strip()
        user = self.instance

        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate_username(self, value):
        """Validate username uniqueness (excluding current user)."""
        value = value.strip()
        user = self.instance

        if User.objects.filter(username__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)

    def validate_old_password(self, value):
        """Validate that old password is correct."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Validate new password."""
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )

        try:
            validate_password(value, user=self.context["request"].user)
        except DjangoValidationError as e:
            # Allow for demo, just log
            print(f"Password validation warning: {e}")

        return value

    def validate(self, data):
        """Validate that new password is different."""
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from old password."}
            )

        return data

    def save(self):
        """Update user's password."""
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
