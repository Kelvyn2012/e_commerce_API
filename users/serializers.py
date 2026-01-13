from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    email = serializers.EmailField(required=True)  # Email validation built-in

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password_confirm"]
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def validate_email(self, value):
        """
        Validate email format and uniqueness.
        """
        if not value:
            raise serializers.ValidationError("Email is required.")

        # Normalize email to lowercase
        value = value.lower().strip()

        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        # Additional email format validation (EmailField already does basic validation)
        if "@" not in value or "." not in value.split("@")[-1]:
            raise serializers.ValidationError("Please provide a valid email address.")

        return value

    def validate_username(self, value):
        """
        Validate username uniqueness and format.
        """
        if not value:
            raise serializers.ValidationError("Username is required.")

        # Normalize username
        value = value.strip()

        # Check minimum length
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )

        # Check if username already exists (case-insensitive)
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_password(self, value):
        """
        Validate password using Django's password validators.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return value

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return data

    def create(self, validated_data):
        """
        Create user with validated data.
        """
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop("password_confirm", None)

        # Create user with normalized data
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # Create token for the new user
        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with email validation.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate_email(self, value):
        """Normalize email."""
        return value.lower().strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Excludes password changes (use separate endpoint).
    """

    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        """
        Validate email uniqueness (excluding current user).
        """
        value = value.lower().strip()
        user = self.instance

        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate_username(self, value):
        """
        Validate username uniqueness (excluding current user).
        """
        value = value.strip()
        user = self.instance

        if User.objects.filter(username__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """
        Validate new password using Django's validators.
        """
        try:
            validate_password(value, user=self.context["request"].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        """
        Validate that new passwords match.
        """
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "New passwords do not match."}
            )

        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from old password."}
            )

        return data

    def save(self):
        """
        Update user's password.
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
