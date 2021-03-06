from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Base(models.Model):
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    update_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)

    class Meta:
        abstract = True


class Human(models.Model):
    GENDER = (
        ('مرد', _('مرد')),
        ('زن', _('زن'))
    )
    name = models.CharField(_('نام و نام خانوادگی'), max_length=200, null=True)
    father_name = models.CharField(_('نام پدر'), max_length=200, null=True, blank=True)
    national_code = models.CharField(_('کد ملی'), max_length=20, null=True, blank=True)
    gender = models.CharField(_('جنسیت'), max_length=20, choices=GENDER, null=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return '{}'.format(self.name)


class Location(models.Model):
    name = models.CharField(_('نام'), max_length=200)
    address = models.TextField(_('آدرس'), default=None, null=True)
    postal_code = models.CharField(_('کد/شناسه'), max_length=20, default=None, null=True)

    class Meta:
        abstract = True


class Document(models.Model):
    image_upload = models.FileField(_('تصویر'), upload_to='document', null=True)
    description = models.TextField(_('توضیحات'), null=True, default=None, blank=True)

    class Meta:
        abstract = True


class Vehicle(models.Model):
    TYPE = (
        ('CAR', 'car'),
        ('TRUCK', 'truck'),
        ('MOTORCYCLE', 'motorcycle'),
        ('PICKUP_TRUCK', 'pickup truck')
    )
    name = models.CharField(_('location name'), max_length=200)
    card_image = models.ImageField(_('card image'), upload_to='vehicle\card', null=True)
    document_image = models.ImageField(_('document image'), upload_to='vehicle\document', null=True)
    card_number = models.CharField(_('card number'), max_length=200, null=True)
    vehicle_number = models.CharField(_('vehicle number'), max_length=200, null=True)
    vehicle_type = models.CharField(_('type'), max_length=50, choices=TYPE)

    class Meta:
        abstract = True


class Building(models.Model):
    TYPE = (
        ('CIVILIAN', 'Civilian'),
        ('RENTAL', 'truck'),
        ('PAWNSHOP', 'pawnshop')
    )

    name = models.CharField(_('building name'), max_length=200)
    postal_code = models.CharField(_('postal code'), max_length=200, null=True)
    address = models.TextField(_('postal code'))
    building_type = models.CharField(_('type'), max_length=50, choices=TYPE)

    class Meta:
        abstract = True




