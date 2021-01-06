from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email_from_template(subject='', recipient_list=None, template='', template_variables=None):
    if template_variables is None:
        template_variables = {}
    template_variables['site_url'] = f'{settings.NETWORK_PROTOCOL}://{settings.DOMAIN}/'
    from_email = settings.EMAIL_ADDRESS
    message = render_to_string(template, template_variables)
    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)


def get_image_url(image_path):
    if image_path:
        return f'{settings.NETWORK_PROTOCOL}://{settings.DOMAIN}/media/{image_path}'
    else:
        return None
