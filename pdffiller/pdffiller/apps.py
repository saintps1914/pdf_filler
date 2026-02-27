from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError


class PdffillerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pdffiller"

    def ready(self) -> None:
        # Create a default admin user for simple deployments.
        username = getattr(settings, "DEFAULT_ADMIN_USERNAME", "admin")
        password = getattr(settings, "DEFAULT_ADMIN_PASSWORD", "admin")
        email = getattr(settings, "DEFAULT_ADMIN_EMAIL", "")

        try:
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
        except (OperationalError, ProgrammingError):
            # Database not ready (e.g., before migrations).
            pass
