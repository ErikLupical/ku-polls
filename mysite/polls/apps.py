from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging

logger = logging.getLogger('polls')

def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        # Connect the signals to handlers
        user_logged_in.connect(log_user_login)
        user_logged_out.connect(log_user_logout)
        user_login_failed.connect(log_login_failed)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    logger.info(f"User {user.username} logged in from IP {ip}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    logger.info(f"User {user.username} logged out from IP {ip}")

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    logger.warning(f"Unsuccessful login attempt for {credentials.get('username')} from IP {ip}")