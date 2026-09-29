"""
Email notifications for the rental request workflow.

Kept in their own module (rather than inline in views.py) so the
notification logic is easy to find, test, and reuse. Every function
uses fail_silently=True so a broken email backend never breaks the
actual request/accept/reject/cancel action for the user.
"""

import logging
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

import mimetypes
import os

logger = logging.getLogger(__name__)


def send_new_request_email(rental_request):
    """Tell the property owner a tenant has requested their property,
    with the property's main/cover photo attached, if it has one."""
    owner = rental_request.property.owner
    if not owner.email:
        return

    property_obj = rental_request.property
    subject = f"New rental request for \"{property_obj.title}\""
    message = (
        f"Hi {owner.username},\n\n"
        f"{rental_request.tenant.username} has requested to rent your property "
        f"\"{property_obj.title}\" ({property_obj.location}).\n\n"
        f"Message from the tenant:\n{rental_request.message or '(no message provided)'}\n\n"
        f"Log in to your dashboard to accept or reject this request.\n\n"
        f"— ঘরবাড়ি (GhorBari)"
    )

    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email])

    if property_obj.image:
        try:
            content_type, _ = mimetypes.guess_type(property_obj.image.name)
            property_obj.image.open('rb')
            email.attach(
                os.path.basename(property_obj.image.name),
                property_obj.image.read(),
                content_type or 'application/octet-stream',
            )
        except Exception:
            logger.exception("Could not attach cover photo for property %s", property_obj.pk)
        finally:
            property_obj.image.close()

    try:
        email.send(fail_silently=False)
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email], fail_silently=False)
    except Exception:
        logger.exception("Failed to send new-request email to %s", owner.email)

"""
    Why the switch from send_mail to EmailMessage

    send_mail() only sends plain text — it has no attachment support. 
    EmailMessage is the lower-level class it's built on, and it exposes .attach(filename, content, mimetype) for exactly this. 
    I used mimetypes.guess_type() rather than hardcoding image/png or image/jpeg, so it works correctly whatever format the owner uploaded (JPEG, PNG, WebP, etc.).

    Behavior notes :
    - If the property has no cover image, the email still sends fine, just without an attachment — no crash.
"""

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
        f"— ঘরবাড়ি (GhorBari)"
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
        f"— ঘরবাড়ি (GhorBari)"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email], fail_silently=False)
    except Exception:
        logger.exception("Failed to send rental cancel request email to %s", owner.email)