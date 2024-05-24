from rest_framework.exceptions import ValidationError
from .models import UserAccount
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.encoding import force_text


UserModel: UserAccount = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAccountSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False, allow_blank=True, max_length=60,
        error_messages={"max_length": "full_name must be less than 60 charecters."})

    class Meta:
        model = UserAccount
        exclude = ["user_permissions", "groups"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, email):
        if UserAccount.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class PasswordResetSerializer(serializers.Serializer):
    """
    Custom Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""

        extra_email_context = {
            "WEBSITE_BASE_URL": settings.WEBSITE_BASE_URL,
            "user_name": self.user.get_full_name() or self.user.username
        }
        return {
            'subject_template_name': 'reset-password-subject.txt',
            'html_email_template_name': 'reset-password-email.html',
            'email_template_name': 'reset-password-email.txt',
            'extra_email_context': extra_email_context
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        
        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('No account found for that email address')
        
        # set user to the class so that we can access it from other methods
        self.user = UserModel.objects.get(email=value)
        
        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(
        max_length=128,
        error_messages={
            'required': "Current password is required",
            'blank': "Please enter your current password"
        }
    )
    new_password1 = serializers.CharField(
        max_length=128,
        error_messages={
            'required': "New password is required",
            'blank': "Please enter a new password"
        }
    )
    new_password2 = serializers.CharField(
        max_length=128,
        error_messages={
            'required': "Confirm password is required",
            'blank': "Please enter confirm password"
        }
    )

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
        
    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError("Current password didn't match")
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()


class AccountUpdateSerializer(serializers.Serializer):

    name = serializers.CharField(
        error_messages={
            'required': 'Name is required',
            'blank': 'Please enter your name'
        }
    )
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required',
            'blank': "Please enter a valid email address"
        }
    )

    def validate_email(self, value):
        user = self.context['request'].user
        
        # check if this email is already exist
        user = UserModel.objects.filter(email=value).exclude(email=user.email).first()

        if user:
            raise ValidationError("This email is already using by another user")
        return value

    def save(self, **kwargs):
        request = self.context['request']
        user = request.user
        
        user.email = self.validated_data.get('email')

        splitted_name = self.validated_data.get('name', '').split(" ")
        if len(splitted_name) == 1:
            user.first_name = splitted_name[0]
        
        else:
            user.first_name = splitted_name[0]
            splitted_name.pop(0)
            user.last_name = " ".join(splitted_name)
        
        user.save()
        return UserAccountSerializer(user, context={"request": request}).data
