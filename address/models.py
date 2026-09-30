from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


class Province(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='استان',
    )

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='شهر',
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name='استان',
    )

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'
        ordering = ('name',)

        constraints = [
            models.UniqueConstraint(
                fields=('name', 'province'),
                name='unique_city_for_province',
                violation_error_message=(
                    'این شهر قبلاً در این استان ثبت شده است.'
                ),
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='کاربر',
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='addresses',
        verbose_name='استان',
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='addresses',
        verbose_name='شهر',
    )

    postal_code = models.CharField(
        max_length=10,
        verbose_name='کد پستی',
    )

    body = models.TextField(
        verbose_name='آدرس کامل',
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name='آدرس پیش‌فرض',
    )

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس‌ها'

        constraints = [
            models.UniqueConstraint(
                fields=('user',),
                condition=models.Q(is_default=True),
                name='unique_default_address_per_user',
                violation_error_message=(
                    'هر کاربر فقط می‌تواند یک آدرس پیش‌فرض داشته باشد.'
                ),
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        if (
                self.province_id
                and self.city_id
                and self.city.province_id != self.province_id
        ):
            errors['city'] = (
                'شهر انتخاب‌شده متعلق به استان انتخاب‌شده نیست.'
            )

        if self.is_default and self.user_id:
            exists = Address.objects.filter(
                user_id=self.user_id,
                is_default=True,
            ).exclude(pk=self.pk).exists()

            if exists:
                errors['is_default'] = (
                    'این کاربر قبلاً یک آدرس پیش‌فرض دارد.'
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f'{self.city} - {self.body}'
