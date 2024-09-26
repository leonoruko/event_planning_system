from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import RSVP
from django.utils.html import strip_tags
import logging

logger=logging.getLogger(__name__)
def check_rsvp(guest):
    try:
        rsvp=RSVP.objects.get(guest=guest.id)
        if rsvp.status=="Attending":
            return rsvp
        else:
            return None
    except:
        return None

def send_invitation(guest,event):
    subject=f"You are invited to {event.event_name}"
    message=render_to_string("emails/invitation_email.html",{"guest":guest,"event":event})
    recipient_email=guest.email
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False
        )
        logger.info(f"Invitation sent to {guest.email} for event {event.event_name}")
    except Exception as e:
        logger.error(f"Failed to send invitation to {guest.email}: {str(e)}")

def send_event_cancellation_email(guest,event):
    subject=f"Event Cancellation:{event.name}"
    message=render_to_string("emails/cancellation_email.html",{"guest":guest,"event":event})
    recipient_email=guest.email    
    if check_rsvp(guest):
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False
            )
            logger.info(f"Cancellation email sent successfully for event {event.event_name}")
        except Exception as e:
            logger.error(f"Failed to send cancellation email to {guest.email}: {str(e)}")


def send_event_reminder_email(guest,event,time_remaining):
    subject=f"Reminder: {event.name} is starting in {time_remaining} "
    message=render_to_string("emails/reminder_email.html",{"guest":guest,"event":event})
    recipient_email=guest.email

    if check_rsvp(guest):
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False
            )
            logger.info(f"Reminder email sent to {guest.email} for event {event.name} starting in {time_remaining}")
        except Exception as e:
            logger.error(f"Failed to send reminder email to {guest.email}: {str(e)}")