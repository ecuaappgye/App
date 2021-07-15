from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class Email(models.Model):
    user = models.ForeignKey("users.BaseUser",
                            on_delete=models.CASCADE,
                            related_name="emails")
    subject = models.CharField(max_length=50)
    body_html = models.CharField(max_length=250)
    body_text = models.CharField(max_length=250)
    date_sent = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        app_label = 'communication'
        ordering = ['-date_sent']
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    def __str__(self) -> str:
        return "%s con propósito de %s" % (self.user.email, self.user.subject)


class CommunicationEventType(models.Model):
    name = models.CharField(max_length=20)
    
    USER_RELATED = "User related"
    DRIVER_RELATED = "Driver related"
    SUPERVISOR_RELATED = "Supervisor related"
    CATEGORY_CHOICES = (
        (USER_RELATED, "USER_RELATED"),
        (DRIVER_RELATED, "DRIVER_RELATED"),
        (SUPERVISOR_RELATED, "SUPERVISOR_RELATED")
    ) 
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)

    email_subject_template = models.CharField(
        _('Email Subject Template'), max_length=255, blank=True, null=True)
    email_body_template = models.TextField(
        _('Email Body Template'), blank=True, null=True)
    email_body_html_template = models.TextField(
        _('Email Body HTML Template'), blank=True, null=True,
        help_text=_("HTML template"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



