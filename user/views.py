from rest_framework.response import Response
from common.views import LoggerAPIView
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer
)
from rest_framework.permissions import AllowAny
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView


class LoginView(BaseLoginView):
    template_name = 'user/login.html'


class LogoutView(BaseLogoutView):
    template_name = 'user/logout.html'


class PasswordChangeView(LoggerAPIView):
    """Modify rest auth default password change view"""

    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully."})


class PasswordResetAPIView(LoggerAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return self.send_200({"detail": "Password reset e-mail has been sent."})


class PasswordResetConfirmAPIView(LoggerAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters:
    token, uid, new_password1, new_password2
    Returns the success/fail message.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.send_200({"detail": "Password has been reset with the new password."})

