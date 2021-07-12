from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    email = models.EmailField(unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Email atribute used to validate session
    USERNAME_FIELD = "email"

    # Fields required by createsuperuser
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Reference to managers object
    objects = BaseUserManager()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self)->str:
        return self.email
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def full_name(self)->str:
        full_name = "%s %s" % (self.first_name.title(), self.last_name.title())
        return full_name.strip()

    def is_staff(self):
        return self.is_admin



