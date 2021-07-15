from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class Email(models.Model):
    user = models.ForeignKey("users.BaseUser",
                            on_delete=models.CASCADE,
                            related_name="emails")
    subject = models.TextField(null=True, blank=True)
    body_html = models.TextField(null=True, blank=True)
    body_text = models.TextField(null=True, blank=True)
    date_sent = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        app_label = 'communication'
        ordering = ['-date_sent']
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    def __str__(self) -> str:
        return "%s con propósito de %s" % (self.user.email, self.user.subject)


class CommunicationEventType(models.Model):
    code = models.CharField(max_length=20)
    
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

    email_subject_template_file = 'communication/emails/commtype_%s_subject.txt'
    email_body_template_file = 'communication/emails/commtype_%s_body.txt'
    email_body_html_template_file = 'communication/emails/commtype_%s_body.html'

    def __str__(self):
        return self.name



