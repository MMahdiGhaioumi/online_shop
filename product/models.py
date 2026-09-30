from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='نام دسته‌بندی',
    )

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='نام اندازه',
    )

    class Meta:
        verbose_name = 'اندازه'
        verbose_name_plural = 'اندازه‌ها'

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='نام رنگ',
    )

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ‌ها'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='نام کالا',
    )

    description = models.TextField(
        verbose_name='توضیحات کامل درباره کالا',
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='ثبت‌کننده',
    )

    category = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name='دسته‌بندی‌ها',
    )

    inventory = models.PositiveIntegerField(
        default=0,
        verbose_name='موجودی',
    )

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'

    def __str__(self) -> str:
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='کالا',
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='product_variants',
        verbose_name='اندازه',
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='product_variants',
        verbose_name='رنگ',
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='کد کالا',
    )

    price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name='قیمت',
    )

    inventory = models.PositiveIntegerField(
        default=0,
        verbose_name='موجودی',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    class Meta:
        verbose_name = 'تنوع کالا'
        verbose_name_plural = 'تنوع کالاها'

        constraints = [
            models.UniqueConstraint(
                fields=('product', 'size', 'color'),
                name='unique_product_variant',
            ),
        ]

    def __str__(self) -> str:
        parts = [self.product.name]

        if self.size:
            parts.append(str(self.size))

        if self.color:
            parts.append(str(self.color))

        return ' - '.join(parts)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='کالا',
    )

    image = models.ImageField(
        upload_to='products/images/',
        verbose_name='نگاره کالا',
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name='نگاره پیش‌فرض',
    )

    class Meta:
        verbose_name = 'نگاره کالا'
        verbose_name_plural = 'نگاره‌های کالا'

    def clean(self):
        super().clean()

        if self.is_default and self.product_id:
            exists = ProductImage.objects.filter(
                product_id=self.product_id,
                is_default=True,
            ).exclude(pk=self.pk).exists()

            if exists:
                raise ValidationError({
                    'is_default': (
                        'این کالا قبلاً یک تصویر پیش‌فرض دارد.'
                    )
                })

    def __str__(self) -> str:
        return self.product.name


class Attribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name='کالا',
    )

    name = models.CharField(
        max_length=128,
        verbose_name='نام ویژگی',
    )

    value = models.CharField(
        max_length=512,
        verbose_name='مقدار ویژگی',
    )

    class Meta:
        verbose_name = 'ویژگی کالا'
        verbose_name_plural = 'ویژگی‌های کالا'

    def __str__(self) -> str:
        return f'{self.name} -- {self.value}'


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'درصدی'
        FIXED = 'fixed', 'مبلغ ثابت'

    name = models.CharField(
        max_length=255,
        verbose_name='نام تخفیف',
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='کد تخفیف',
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        verbose_name='نوع تخفیف',
    )

    value = models.PositiveBigIntegerField(
        verbose_name='مقدار تخفیف',
    )

    start_at = models.DateTimeField(
        verbose_name='شروع تخفیف',
    )

    end_at = models.DateTimeField(
        verbose_name='پایان تخفیف',
    )

    min_order_amount = models.PositiveBigIntegerField(
        default=0,
        verbose_name='حداقل مبلغ سفارش',
    )

    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='حداکثر تعداد استفاده',
    )

    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد استفاده',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='discounts',
        verbose_name='کالاها',
    )

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='discounts',
        verbose_name='دسته‌بندی‌ها',
    )

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def clean(self):
        super().clean()

        errors = {}

        if self.discount_type == self.DiscountType.PERCENTAGE:
            if not 1 <= self.value <= 100:
                errors['value'] = (
                    'درصد تخفیف باید بین ۱ تا ۱۰۰ باشد.'
                )

        if self.start_at and self.end_at:
            if self.end_at <= self.start_at:
                errors['end_at'] = (
                    'پایان تخفیف باید بعد از شروع آن باشد.'
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        PAID = 'paid', 'پرداخت شده'
        PROCESSING = 'processing', 'در حال پردازش'
        SHIPPED = 'shipped', 'ارسال شده'
        DELIVERED = 'delivered', 'تحویل داده شده'
        RETURNED = 'returned', 'برگشت داده شده'
        CANCELLED = 'cancelled', 'لغو شده'

    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='شماره سفارش',
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='کاربر',
    )

    address = models.ForeignKey(
        'address.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='آدرس',
    )

    # Snapshot آدرس در زمان ثبت سفارش
    shipping_province = models.CharField(
        max_length=128,
        verbose_name='استان ارسال',
    )

    shipping_city = models.CharField(
        max_length=128,
        verbose_name='شهر ارسال',
    )

    shipping_address = models.TextField(
        verbose_name='آدرس ارسال',
    )

    shipping_postal_code = models.CharField(
        max_length=10,
        verbose_name='کد پستی ارسال',
    )

    # اطلاعات مالی
    subtotal = models.PositiveBigIntegerField(
        default=0,
        verbose_name='جمع قیمت کالاها',
    )

    discount_amount = models.PositiveBigIntegerField(
        default=0,
        verbose_name='مبلغ تخفیف',
    )

    shipping_cost = models.PositiveBigIntegerField(
        default=0,
        verbose_name='هزینه ارسال',
    )

    total_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name='مبلغ نهایی سفارش',
    )

    discount_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='کد تخفیف',
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name='وضعیت سفارش',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت سفارش',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین تغییر',
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ('-created_at',)

    def __str__(self):
        if self.user:
            return (
                f'سفارش {self.order_number} - '
                f'{self.user.phone_number}'
            )

        return f'سفارش {self.order_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='کالا',
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name='تنوع کالا',
    )

    # Snapshot اطلاعات کالا
    product_name = models.CharField(
        max_length=512,
        verbose_name='نام کالا',
    )

    variant_description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name='مشخصات تنوع',
    )

    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='تعداد',
    )

    # قیمت در لحظه خرید
    price = models.PositiveBigIntegerField(
        verbose_name='قیمت واحد (تومان)',
    )

    discount_amount = models.PositiveBigIntegerField(
        default=0,
        verbose_name='مبلغ تخفیف',
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    @property
    def total_price(self):
        return max(
            self.subtotal - self.discount_amount,
            0,
        )

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
        ordering = ('-order__created_at',)

    def __str__(self):
        return self.product_name
