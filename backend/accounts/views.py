from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .serializers import LoginSerializer, PasswordResetConfirmSerializer, RegisterSerializer, UserSerializer

def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh), 'user': UserSerializer(user).data}

def verification_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk)); token = default_token_generator.make_token(user)
    return f'{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}'

class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer=RegisterSerializer(data=request.data); serializer.is_valid(raise_exception=True); user=serializer.save()
        response_data = tokens_for(user)
        response_data['message'] = 'Account created successfully! Welcome to FoodGuard.'
        return Response(response_data, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        try: user=User.objects.get(pk=force_str(urlsafe_base64_decode(request.data.get('uid',''))))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError): return Response({'detail':'Invalid verification link.'}, status=400)
        if not default_token_generator.check_token(user, request.data.get('token','')): return Response({'detail':'Invalid or expired verification link.'}, status=400)
        user.is_active=True; user.save(update_fields=['is_active'])
        return Response({'message':'Email verified. You can now sign in.'})

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer=LoginSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        return Response(tokens_for(serializer.validated_data['user']))

class LogoutView(APIView):
    def post(self, request):
        try: RefreshToken(request.data['refresh']).blacklist()
        except Exception: return Response({'detail':'Invalid refresh token.'}, status=400)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MeView(APIView):
    def get(self, request): return Response(UserSerializer(request.user).data)

class PasswordResetRequestView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        email=request.data.get('email','').lower().strip(); user=User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            uid=urlsafe_base64_encode(force_bytes(user.pk)); token=default_token_generator.make_token(user)
            send_mail('Reset your FoodGuard password', f'Reset your password: {settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}', settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'message':'If an account exists, we sent password reset instructions.'})

class PasswordResetConfirmView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer=PasswordResetConfirmSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        try: user=User.objects.get(pk=force_str(urlsafe_base64_decode(request.data.get('uid',''))))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError): return Response({'detail':'Invalid reset link.'}, status=400)
        if not default_token_generator.check_token(user, request.data.get('token','')): return Response({'detail':'Invalid or expired reset link.'}, status=400)
        user.set_password(serializer.validated_data['password']); user.save()
        return Response({'message':'Password reset successfully. You can now sign in.'})
