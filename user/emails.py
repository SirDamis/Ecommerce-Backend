from graphql_auth.constants import TokenAction
from graphql_auth.settings import graphql_auth_settings as app_settings
from graphql_auth.utils import get_token_paylod

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_welcome_email(token):
    payload = get_token_paylod(
        token, TokenAction.ACTIVATION
    )

    email = payload['email']
    print(email)
    html_template = get_template('email/welcome.html')
    comtext = {
        'email': email,
    }
    
    subject, from_email, to = 'Welcome to Ecommerce', 'noreply@ecommerce.com', email
    html_content = html_template.render(comtext)
    msg =  EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.send()