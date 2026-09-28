from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        OWNER = 'owner', 'مالک'
        MANAGER = 'manager', 'مدیر'
        SELLER = 'seller', 'فروشنده'
        CUSTOMER = 'customer', 'مشتری'

    phone_number = models.CharField(max_length=50, unique=True, verbose_name='شماره همراه')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام خانوادگی')
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER, verbose_name='نقش')
    birth_date = models.DateField(verbose_name='تاریخ تولد', null=True, blank=True)
    image = models.ImageField(upload_to='images/profile', null=True, blank=True, verbose_name='نگاره شخصی')
    date_joined = models.DateTimeField(verbose_name='تاریخ عضویت', default=timezone.now)
    is_staff = models.BooleanField(
        verbose_name='وضعیت کارکنان',
        default=False,
        help_text='مشخص می‌کند که آیا کاربر می‌تواند به این سایت مدیریتی وارد شود یا خیر.'
    )
    is_active = models.BooleanField(
        verbose_name='این کاربر فعال است',
        default=True,
        help_text=(
            'مشخص می‌کند که آیا این کاربر باید به عنوان کاربر فعال در نظر گرفته شود یا خیر.'
            'به‌جای حذف حساب‌ها، تیک این گزینه را بردارید.'
        )
    )

    objects = managers.UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر‌ها'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.phone_number