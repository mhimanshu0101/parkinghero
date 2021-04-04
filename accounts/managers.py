from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_active, is_superuser, **extra_fields):
        """
        Create and save user with the given email and password.
        """
        now = timezone.localtime(timezone.now())
        user = self.model(
            email=email, is_active=is_active,
            is_staff=is_staff, is_superuser=is_superuser,
            last_login=now, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        is_active = extra_fields.pop('is_active', False)
        return self._create_user(email, password, False, is_active, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)