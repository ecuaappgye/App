from django.db import models


class CallBackTokenManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)
    
    def inactive(self):
        return self.get_queryset().filter(is_active=False)