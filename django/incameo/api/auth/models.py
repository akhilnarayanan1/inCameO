from django.db import models
from uuid import uuid4
from .validators import AlphanumericUsernameValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, user_username, user_email, user_fullname, user_dob=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not user_email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_username=user_username,
            user_email=self.normalize_email(user_email),
            user_fullname=user_fullname,
            user_dob=user_dob,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_username, user_email, user_fullname, user_dob=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            user_username=user_username,
            user_email=user_email,
            user_fullname=user_fullname,
            user_dob=user_dob,
            password=password,
        )
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.UUIDField(
        primary_key = True,
        default = uuid4,
    )
    user_fullname = models.CharField(
        verbose_name='full name',
        max_length=50,
    )
    user_username = models.CharField(
        verbose_name='username',
        max_length=15,
        unique=True,
        validators=[AlphanumericUsernameValidator]
    )
    user_email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_dob = models.DateField(
      blank=True, null=True
    )
    is_verified = models.BooleanField(
            default=False,
            help_text="Designates whether this user is verified. Unselect this if user not verified."
        )
    is_active = models.BooleanField(
            default=True,
            help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='staff status',
        help_text="Designates whether this user should be treated as staff. Staff users can login to Admin"
    )
    is_superuser = models.BooleanField(
            default=False,
            verbose_name='superuser status',
            help_text="Designates that this user has all permissions without explicitly assigning them."
        )
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_fullname', 'user_username']

    def __str__(self):
        return self.user_email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
