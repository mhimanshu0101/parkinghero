from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.management.utils import get_random_secret_key

from django.utils import timezone
from .managers import UserManager

now = timezone.localtime(timezone.now())

# Create your models here.
class UserType:
    EMPLOYEE = 1
    PARTNER = 2
    CUSTOMER = 3

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICE = (
        (None, 'Please select user type'),
        (UserType.EMPLOYEE, 'Employee'),
        (UserType.PARTNER, 'Partner'),
        (UserType.CUSTOMER, 'Customer')
    )
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICE, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    token_secret_key = models.CharField(max_length=128, default=get_random_secret_key, unique=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.email or self.id or ''