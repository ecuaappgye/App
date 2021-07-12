from django.contrib.auth.models import BaseUserManager as BUM

from .utils import validate_password


class BaseUserManager(BUM):
    def create_user(
        self, 
        first_name, 
        last_name, 
        email, 
        password,
        is_active=True,
        is_admin=False):

        if not email:
            raise ValueError("Email requerido")
        
        user = self.model(
            first_name=first_name,
            last_name= last_name,
            email=self.normalize_email(email),
            is_admin=is_admin,
            is_active=is_active)

        if password is not None:
            validate_password(password=password, user=user)
            user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(
        self, 
        first_name, 
        last_name, 
        email, 
        password):
        user = self.create_user(first_name, last_name, email, password, is_active=True, is_admin=True)
        user.is_superuser = True
        user.save(using=self._db)

        return user
