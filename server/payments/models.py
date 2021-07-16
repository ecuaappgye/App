from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Retention (models.Model):
    service_total = models.FloatField(validators=[MinValueValidator(0.9),MaxValueValidator(100)])
    service_supervisor = models.FloatField(validators=[MinValueValidator(0.9),MaxValueValidator(100)])
    service_app = models.FloatField(validators=[MinValueValidator(0.9),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.service_total:
            raise ValidationError ("El servicio total no puede estar vacío")
        if not self.service_supervisor:
            raise ValidationError("El servicio total no puede estar vacío")
        if not self.service_app:
            raise ValidationError("El servicio total no puede estar vacío") 
        if self.service_supervisor + self.service_app > 100: 
            raise ValidationError ("El servicio de retención del supervisor y de la aplicación supera el 100%")
        if self.service_total > 100:
            raise ValidationError ("El servicio total supera el 100%")
                
    def __str__(self) -> str:
        return "Retención con fecha %s" % (self.created_at)

    def save(self,*args , **kwargs):
        self.full_clean()
        return super().save(*args , **kwargs)
    
    

    