from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class Role(models.TextChoices):
    """Application-level roles. Ordered lowest to highest in ROLE_ORDER below."""

    MEMBER = "member", "Member"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"


ROLE_ORDER = [Role.MEMBER, Role.MANAGER, Role.ADMIN]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(email=self.normalize_email(email).lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Email-as-username user. Set up from day one: swapping the user model later is painful."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        ordering = ["-date_joined"]
        constraints = [
            # Choices are only validated in forms/serializers; this protects the column itself.
            models.CheckConstraint(
                condition=models.Q(role__in=Role.values), name="users_user_role_valid"
            ),
        ]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # case-insensitive uniqueness
        super().save(*args, **kwargs)

    def has_min_role(self, minimum: str) -> bool:
        """True if the user's role is at least `minimum`. Superusers always pass."""
        if self.is_superuser:
            return True
        return ROLE_ORDER.index(Role(self.role)) >= ROLE_ORDER.index(Role(minimum))

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name or self.email
