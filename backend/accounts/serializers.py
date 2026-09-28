from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=12, style={'input_type':'password'})
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value
    def validate_password(self, value):
        validate_password(value)
        if not any(c.isupper() for c in value) or not any(c.islower() for c in value) or not any(c.isdigit() for c in value):
            raise serializers.ValidationError('Use upper- and lowercase letters and at least one number.')
        return value
    def create(self, validated_data):
        email = validated_data['email']
        user = User(email=email, username=email, first_name=validated_data.get('first_name',''), last_name=validated_data.get('last_name',''))
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    def validate(self, attrs):
        candidate = User.objects.filter(email__iexact=attrs['email'].lower()).first()
        if candidate and not candidate.is_active:
            raise serializers.ValidationError('Please verify your email before signing in.')
        user = authenticate(username=attrs['email'].lower(), password=attrs['password'])
        if not user: raise serializers.ValidationError('Invalid email or password.')
        attrs['user'] = user
        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=12)
    def validate_password(self, value):
        validate_password(value)
        if not any(c.isupper() for c in value) or not any(c.islower() for c in value) or not any(c.isdigit() for c in value):
            raise serializers.ValidationError('Use upper- and lowercase letters and at least one number.')
        return value
