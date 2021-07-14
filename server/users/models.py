from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)

    # Check if admin of active to session
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    rol = models.ForeignKey("users.Rol", null=True, blank=True, on_delete=models.CASCADE)
    document = models.ForeignKey("users.Document", null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Atributo de inicio de sesión.
    USERNAME_FIELD = "email"

    # Atributo de creación de superadministrador.
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Reference to managers object
    objects = BaseUserManager()

    DRIVER = "conductor"
    CLIENT = "cliente"
    
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

    @property
    def rol_name(self):
        if not self.rol:
            return None
        return self.rol.name

    @ property
    def is_driver(self):
        if not self.rol:
            return None
        return self.rol.name.lower() == self.DRIVER
    
    @ property
    def is_client(self):
        if not self.rol:
            return None
        return self.rol.name.lower() == self.CLIENT

    def is_staff(self):
        return self.is_admin
    
    def user_send_mail(self, subject, message, from_email, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Rol(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100,
        help_text="Descripción de tareas a realizar por el rol.")

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

    
class Document(models.Model):
    cedula_img = models.ImageField(upload_to="cedula_img")
    licencia_img = models.ImageField(upload_to="licencia_img")
    matricula_img = models.ImageField(upload_to="matricula_img")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


