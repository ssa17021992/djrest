from django.core.mail import EmailMessage

from djrest.celery import app

from .utils import send_notification


@app.task
def add(a, b):
    """Add"""
    return a + b


@app.task
def send_fcm_notification(*args, **kwargs):
    """Send fcm notification"""
    send_notification(*args, **kwargs)


@app.task
def send_mail(subject, body, to):
    """Send mail"""
    msg = EmailMessage(subject=subject, body=body, to=[to])
    return msg.send(fail_silently=True)
