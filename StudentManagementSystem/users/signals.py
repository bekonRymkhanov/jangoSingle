import logging
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.timezone import now

# Get the logger instance
logger = logging.getLogger('users')

# Get the User model
User = get_user_model()

# Log user registration
@receiver(post_save, sender=User)
def log_user_created(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"[{now()}] New user registered: {instance.email} (ID: {instance.id})"
        )
        print(f"Signal fired for user creation: {instance.email}")  # Optional debug print


# Log user login
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(
        f"[{now()}] User logged in: {user.email} (ID: {user.id}) | IP: {get_client_ip(request)}"
    )


# Log user logout
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(
        f"[{now()}] User logged out: {user.email} (ID: {user.id}) | IP: {get_client_ip(request)}"
    )


# Utility function to get client IP address
def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip