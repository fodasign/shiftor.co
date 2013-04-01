"""Email handling."""

import logging
logger = logging.getLogger(__name__)
from smtplib import SMTPServerDisconnected

# Django imports
from django.conf import settings
from django.core import urlresolvers
from django.core.mail import send_mail
from django.contrib import auth
from django.template import Context
from django.template.loader import get_template

User = auth.get_user_model()

def verify (request, **kwargs):
    title = "Silk Tradr: Please verify your email address!"
    template = "emails/verify.html"
    to_email = [kwargs.get("to")]
    from_email = "helper@silktradr.com"
    context = Context(kwargs)
    body = get_template(template).render(context)
    return title, body, from_email, to_email

def verify_admin (request, **kwargs):
    title, body, from_email, to_email = verify(request, **kwargs)
    to_email = get_admin_emails()
    return title, body, from_email, to_email

def thread_response (request, user=None, message=None, thread=None, **kwargs):
    title = "{user.name} sent you a message about {item}".format(user=user, item=thread.item)
    template = "emails/thread_response.html"
    to_email = [user.email]
    from_email = "helper@silktradr.com"
    thread_link = request.build_absolute_uri(urlresolvers.reverse("messages.views.view_thread", kwargs={"pk" : thread.pk}))
    context = Context({ "message" : message, "thread_link" : thread_link })
    body = get_template(template).render(context)
    return title, body, from_email, to_email

def administrative (request, **kwargs):
    title = "A general information email about {subject}".format(subject=kwargs.get("subject"))
    template = "emails/administrative.html"
    to_email = get_admin_emails()
    from_email = "helper@silktradr.com"
    context = Context({ "cause" : kwargs.get("subject"), "other_vars" : kwargs })
    body = get_template(template).render(context)
    return title, body, from_email, to_email

def get_admin_emails ():
    """
    Helper function that returns a list of emails from users that are
    in the mailers group.
    """
    return [ user.email for user in User.objects.filter(is_staff=True)]

def _process_hooks (request, email, **kwargs):
    """Processed admin hooks for emails, called after send is executed."""
    logger.debug("Processing remaining hooks for {0}".format(email))
    if email in ["verify"]:
        logger.debug("Admin hook found for {0}".format(email))
        admin_func = EMAIL_MAP.get("{0}_admin".format(email))
        send_mail(*admin_func(request, **kwargs))

EMAIL_MAP = {
    "verify" : verify,
    "verify_admin" : verify_admin,
    "thread_response" : thread_response,
    "administrative" : administrative,
}

def send (request, email, **kwargs):
    """
    Handles sending an email defined by the email parameter. Email is defined
    as a function in this file which is executed with the corrosponding :data:`**kwargs`
    and request object.
    """
    logger.debug("Attempting to send an {0} email".format(email))
    # Dig the template out of our available functions
    template = EMAIL_MAP.get(email)
    if template is None:
        raise LookupError("Unable to find template function {0}".format(email))

    logger.debug("Executing {0} with arguments {1}".format(template, kwargs))
    try:
        send_mail(*template(request, **kwargs), fail_silently=False)
        _process_hooks(request, email, **kwargs)
    except SMTPServerDisconnected as e:
        logger.exception(e)
        logger.error("Unable to send email, SMTPServerDisconnected")