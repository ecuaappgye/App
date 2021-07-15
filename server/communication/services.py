from server.communication.models import CommunicationEventType
from django.conf import settings
from django.template import engines
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template


def communication_event_type_get_messages(*, event: CommunicationEventType, code: str, ctx=None):
    """Return a dict of templates with the context merged in

       We look first at the field templates but fail over to
       a set of file templates that follow a conventional path.
    """

    # Build a dict of messages name to Template instances

    templates = {
        'subject': 'email_subject_template',
        'body': 'email_body_template',
        'html': 'email_body_html_template',
    }

    code = code.lower()

    for name, attr_name in templates.items():
        field = getattr(event, attr_name, None)
        if field is not None:
            # Template content is in a model field
            templates[name] = engines['django'].from_string(field)
        else:
            # Model field is empty - look for a file template
            template_name = getattr(event, "%s_file" % attr_name) % code
            try:
                templates[name] = get_template(template_name)
            except TemplateDoesNotExist:
                templates[name] = None

        if ctx is None:
            ctx = {}
            ctx['static_base_url'] = getattr(
                settings, 'STATIC_URL', None)

    messages = {}
    for name, template in templates.items():
        messages[name] = template.render(ctx) if template else ''
        # Ensure the email subject doesn't contain any newlines
        messages['subject'] = messages['subject'].replace("\n", "")
        messages['subject'] = messages['subject'].replace("\r", "")

    return messages


def communication_event_type_get_and_render(*, code: str, context):
    """Return a dictionary of rendered messaged, ready for sending
    If event not exists create event database 
    """
    try:
        event = CommunicationEventType.objects.get(code=code)
    except CommunicationEventType.DoesNotExist:
        event = CommunicationEventType.objects.create(code=code)
    messages = communication_event_type_get_messages(
        event=event,
        code=code,
        ctx=context)
    return messages
