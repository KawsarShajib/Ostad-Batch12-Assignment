"""
Email notifications for the rental request workflow.

Kept in their own module (rather than inline in views.py) so the
notification logic is easy to find, test, and reuse. Every function
uses fail_silently=True so a broken email backend never breaks the
actual request/accept/reject/cancel action for the user.
"""

import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_new_request_email(rental_request):
    """Tell the property owner a tenant has requested their property."""
    owner = rental_request.property.owner
    if not owner.email:
        return

    subject = f"New rental request for \"{rental_request.property.title}\""
    message = (
        f"Hi {owner.username},\n\n"
        f"{rental_request.tenant.username} has requested to rent your property "
        f"\"{rental_request.property.title}\" ({rental_request.property.location}).\n\n"
        f"Message from the tenant:\n{rental_request.message or '(no message provided)'}\n\n"
        f"Log in to your dashboard to accept or reject this request.\n\n"
        f"— PropRental"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email], fail_silently=False)
    except Exception as e:
        logger.exception("Failed to send new-request email to %s", owner.email)



def send_request_status_email(rental_request):
    """Tell the tenant their request was accepted or rejected."""
    tenant = rental_request.tenant
    if not tenant.email:
        return

    status = rental_request.get_status_display().lower()
    subject = f"Your rental request for \"{rental_request.property.title}\" was {status}"
    message = (
        f"Hi {tenant.username},\n\n"
        f"Your rental request for \"{rental_request.property.title}\" "
        f"({rental_request.property.location}) has been {status} by the property owner.\n\n"
        f"Log in to view the details.\n\n"
        f"— PropRental"
    )
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [tenant.email], fail_silently=False)
    except Exception:
        logger.exception("Failed to send rental request email to %s", tenant.email)



def send_request_cancelled_email(rental_request):
    """Tell the property owner that a tenant cancelled their pending request."""
    owner = rental_request.property.owner
    if not owner.email:
        return

    subject = f"Rental request cancelled for \"{rental_request.property.title}\""
    message = (
        f"Hi {owner.username},\n\n"
        f"{rental_request.tenant.username} has cancelled their pending rental request "
        f"for \"{rental_request.property.title}\".\n\n"
        f"— PropRental"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email], fail_silently=False)
    except Exception:
        logger.exception("Failed to send rental cancel request email to %s", owner.email)