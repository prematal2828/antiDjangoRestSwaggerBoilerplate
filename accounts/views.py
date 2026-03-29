"""
Views for the accounts app.
"""

from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import ChangePasswordSerializer, RegisterSerializer, UserProfileSerializer

User = get_user_model()


@extend_schema(tags=["Auth"], summary="Register a new user")
class RegisterView(APIView):
    """Register a new user account."""

    permission_classes = (permissions.AllowAny,)
    serializer_class=RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class LoginView(TokenObtainPairView):
    """Obtain JWT access and refresh tokens (login)."""


@extend_schema(tags=["Auth"])
class TokenRefreshView(TokenRefreshView):
    """Refresh the JWT access token using a valid refresh token."""


@extend_schema(
    tags=["Auth"],
    request={"application/json": {"type": "object", "properties": {"refresh": {"type": "string"}}, "required": ["refresh"]}},
    responses={205: OpenApiResponse(description="Tokens blacklisted, logged out successfully.")},
)
class LogoutView(APIView):
    """Blacklist the refresh token to log out the user."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(summary="Get current user profile"),
    put=extend_schema(summary="Update current user profile (full)"),
    patch=extend_schema(summary="Update current user profile (partial)"),
)
class UserProfileView(APIView):
    """Get or update the authenticated user's profile."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class=UserProfileSerializer

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"], summary="Change password")
class ChangePasswordView(APIView):
    """Change the authenticated user's password."""

    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class=ChangePasswordSerializer

    @extend_schema(
    responses={
        200: inline_serializer(
            name='PasswordChangeSuccess',
            fields={
                'detail': serializers.CharField(default='Password changed successfully.')
            }
        ),
    }
)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
