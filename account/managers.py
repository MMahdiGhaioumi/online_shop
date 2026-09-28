from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):

    def _create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")

        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        extra_fields.setdefault('role', get_user_model().Role.CUSTOMER)

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_unusable_password()
        return user

    def _create_superuser(self, phone_number, password, **extra_fields):
        if not phone_number and not password:
            raise ValueError("The phone number and password must be set")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', get_user_model().Role.OWNER)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        return user

    def create_user(self, phone_number, **extra_fields):
        user = self._create_user(phone_number, **extra_fields)

        user.save(using=self._db)
        return user

    async def acreate_user(self, phone_number, **extra_fields):
        user = self._create_user(phone_number, **extra_fields)

        await user.asave(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self._create_superuser(phone_number, password, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)
        return user

    async def acreate_superuser(self, phone_number, password, **extra_fields):
        user = self._create_superuser(phone_number, password, **extra_fields)

        user.set_password(password)

        await user.asave(using=self._db)
        return user
