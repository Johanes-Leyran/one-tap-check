from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission
# Todo: add feature to authenticate the rfid card of the user
# TODO: make the manager implements custom permissions


class OneTapUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(email, password, **extra_fields)
        """
         A superuser must have all the permissions
        """
        all_permissions = Permission.objects.all()
        user.user_permissions.set(all_permissions)

        return user
