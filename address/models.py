from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


class Province(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='استان',
        unique=True,
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
        verbose_name='استان',
        related_name='cities',
    )

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر‌ها'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'province'],
                name='unique_city_for_province',
                violation_error_message='این شهر قبلاً در این استان ثبت شده است.',
            )
        ]

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='addresses',
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='استان',
        related_name='addresses',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='شهر',
        related_name='addresses',
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name='کدپستی'
    )
    body = models.TextField(verbose_name='آدرس کامل')
    is_default = models.BooleanField(verbose_name='آدرس پیشفرض', default=False)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس‌ها'
        constraints = [
            models.UniqueConstraint(
                fields=('user',),
                condition=models.Q(is_default=True),
                name='unique_address_for_user',
                violation_error_message='هر کاربر فقط یک آدرس پیشفرض دارد.!!',
            )
        ]

    def clean(self) -> None:
        if (self.province_id and self.city_id
                and self.city.province_id != self.province_id):
            raise ValidationError({
                'city': 'شهر انتخاب‌شده متعلق به استان انتخاب‌شده نیست.',
            })

    def __str__(self) -> str:
        return self.body
