from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    cdi = models.CharField(max_length=10, null=True, blank=True)

    # Check if admin of active to session
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Atributo de inicio de sesión.
    USERNAME_FIELD = "email"

    # Atributo de creación de superadministrador.
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
    


class Rol(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100,
        help_text="Descripción de tareas a realizar por el rol.")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')

    def __str__(self)-> str:
        return "Rol %s" % self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class DocumentType(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100,
        help_text="Descripción del tipo de documento.")
    rol = models.ManyToManyField(Rol)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')
    
    def __str__(self) -> str:
        return self.name
